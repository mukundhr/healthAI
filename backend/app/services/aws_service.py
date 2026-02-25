import boto3
import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime
import uuid

from app.core.config import settings

logger = logging.getLogger(__name__)


class AWSService:
    def __init__(self):
        self.s3_client = None
        self.textract_client = None
        self.bedrock_client = None
        self.bedrock_runtime = None
        self.polly_client = None
        self._initialized = False
    
    def initialize_services(self):
        if self._initialized:
            return
            
        logger.info("Initializing AWS services...")
        
        # Create base session
        session = boto3.Session(
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )
        
        # S3 Client
        self.s3_client = session.client('s3')
        
        # Textract Client
        self.textract_client = session.client('textract')
        
        # Bedrock Client (for listing models)
        self.bedrock_client = session.client('bedrock')
        
        # Bedrock Runtime (for invoking models)
        self.bedrock_runtime = session.client('bedrock-runtime')
        
        # Polly Client
        self.polly_client = session.client('polly')
        
        self._initialized = True
        logger.info("AWS services initialized successfully")
    
    async def upload_document(self, file_content: bytes, file_name: str, session_id: str) -> Dict[str, str]:
        try:
            key = f"sessions/{session_id}/documents/{datetime.now().timestamp()}_{file_name}"
            
            self.s3_client.put_object(
                Bucket=settings.AWS_S3_BUCKET,
                Key=key,
                Body=file_content,
                ContentType=self._get_content_type(file_name)
            )
            
            s3_uri = f"s3://{settings.AWS_S3_BUCKET}/{key}"
            logger.info(f"Document uploaded: {s3_uri}")
            
            return {
                "s3_uri": s3_uri,
                "s3_key": key,
                "bucket": settings.AWS_S3_BUCKET
            }
        except Exception as e:
            logger.error(f"S3 upload error: {str(e)}")
            raise
    
    async def download_document(self, s3_key: str) -> bytes:
        try:
            response = self.s3_client.get_object(
                Bucket=settings.AWS_S3_BUCKET,
                Key=s3_key
            )
            return response['Body'].read()
        except Exception as e:
            logger.error(f"S3 download error: {str(e)}")
            raise
    
    async def delete_document(self, s3_key: str):
        try:
            self.s3_client.delete_object(
                Bucket=settings.AWS_S3_BUCKET,
                Key=s3_key
            )
        except Exception as e:
            logger.error(f"S3 delete error: {str(e)}")
    
    async def generate_presigned_url(self, s3_key: str, expiration: int = 3600) -> str:
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': settings.AWS_S3_BUCKET,
                    'Key': s3_key
                },
                ExpiresIn=expiration
            )
            return url
        except Exception as e:
            logger.error(f"Presigned URL error: {str(e)}")
            raise
    
    async def extract_text(self, file_content: bytes, file_name: str) -> Dict[str, Any]:
        try:
            # Determine if PDF or image
            if file_name.lower().endswith('.pdf'):
                # For PDFs, use document analysis
                response = self.textract_client.analyze_document(
                    Document={'Bytes': file_content},
                    FeatureTypes=['TABLES', 'FORMS']
                )
            else:
                # For images
                response = self.textract_client.analyze_document(
                    Document={'Bytes': file_content},
                    FeatureTypes=['TABLES', 'FORMS']
            )
            
            # Extract text blocks
            text_blocks = []
            blocks = response.get('Blocks', [])
            
            for block in blocks:
                if block['BlockType'] == 'LINE':
                    text_blocks.append({
                        'text': block['Text'],
                        'confidence': block.get('Confidence', 0),
                        'page': block.get('Page', 1)
                    })
            
            # Calculate overall confidence
            avg_confidence = sum(b['confidence'] for b in text_blocks) / len(text_blocks) if text_blocks else 0
            
            full_text = '\n'.join([block['text'] for block in text_blocks])
            
            logger.info(f"Textract extracted {len(text_blocks)} text blocks with {avg_confidence:.1f}% confidence")
            
            return {
                'text': full_text,
                'blocks': text_blocks,
                'confidence': avg_confidence,
                'blocks_count': len(text_blocks)
            }
        except Exception as e:
            logger.error(f"Textract error: {str(e)}")
            raise
    
    async def generate_medical_explanation(
        self,
        extracted_text: str,
        language: str = "en",
        user_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        try:
            # Build prompt based on language and context
            prompt = self._build_medical_prompt(extracted_text, language, user_context)
            
            # Invoke Bedrock model
            response = self.bedrock_runtime.invoke_model(
                modelId=settings.AWS_BEDROCK_MODEL_ID,
                contentType="application/json",
                accept="application/json",
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 4096,
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                })
            )
            
            # Parse response
            response_body = json.loads(response['body'].read().decode('utf-8'))
            explanation = response_body['content'][0]['text']
            
            # Extract confidence level
            confidence = self._estimate_confidence(explanation)
            
            # Generate doctor questions
            questions = await self._generate_doctor_questions(extracted_text, language)
            
            return {
                'explanation': explanation,
                'confidence': confidence,
                'language': language,
                'questions': questions,
                'model': settings.AWS_BEDROCK_MODEL_ID
            }
        except Exception as e:
            logger.error(f"Bedrock error: {str(e)}")
            raise
    
    def _build_medical_prompt(self, text: str, language: str, context: Optional[Dict]) -> str:

        lang_instruction = {
            "en": "Respond in English",
            "hi": "Respond in Hindi (हिंदी में जवाब दें)",
            "kn": "Respond in Kannada (ಕನ್ನಡದಲ್ಲಿ ಉತ್ತರಿಸಿ)"
        }.get(language, "Respond in English")
        
        system_prompt = f"""You are AccessAI, a medical report analysis assistant designed to help users understand their health reports in simple language.

IMPORTANT GUIDELINES:
1. {lang_instruction}
2. Use simple, everyday language that anyone can understand
3. Always explain medical terms when you first use them
4. Be transparent about what the AI knows and doesn't know
5. If something is unclear or uncertain, explicitly state "I'm not certain about..."
6. Never provide medical diagnoses - always recommend consulting a doctor
7. Structure your response with clear sections
8. Highlight any values that are outside normal ranges
9. Include a confidence statement about the analysis

CONTEXT: The user has uploaded a medical report. Please analyze and explain it in simple terms."""
        
        user_prompt = f"""{system_prompt}

MEDICAL REPORT TEXT:
---
{text}
---

Please provide:
1. A summary of what this report shows
2. Any values that are outside normal ranges, explained simply
3. What the user should discuss with their doctor
4. A clear statement about your confidence in this analysis

Format your response clearly with headings."""
        
        return user_prompt
    
    async def _generate_doctor_questions(self, text: str, language: str) -> list:
        """Generate questions for the doctor based on the report"""
        try:
            prompt = f"""Based on the following medical report, generate 5 important questions that the patient should ask their doctor. 

{lang_instruction := {
    "en": "Respond in English",
    "hi": "Respond in Hindi",
    "kn": "Respond in Kannada"
}.get(language, "Respond in English")}

MEDICAL REPORT:
{text}

Generate exactly 5 questions, one per line, that would help the patient understand their health better. These should be specific to the findings in the report."""

            response = self.bedrock_runtime.invoke_model(
                modelId=settings.AWS_BEDROCK_MODEL_ID,
                contentType="application/json",
                accept="application/json",
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 1024,
                    "messages": [
                        {"role": "user", "content": prompt}
                    ]
                })
            )
            
            response_body = json.loads(response['body'].read().decode('utf-8'))
            questions_text = response_body['content'][0]['text']
            
            # Parse questions (split by newlines, filter empty)
            questions = [q.strip() for q in questions_text.split('\n') if q.strip() and ('.' in q or '?' in q)]
            
            # Ensure we have exactly 5 questions
            return questions[:5] if len(questions) >= 5 else questions + [""] * (5 - len(questions))
            
        except Exception as e:
            logger.error(f"Question generation error: {str(e)}")
            return []
    
    def _estimate_confidence(self, explanation: str) -> int:
        # Simple heuristic - could be enhanced with ML
        uncertainty_indicators = ["may", "might", "could be", "possibly", "不确定", "अनिश्चित"]
        
        if any(word in explanation.lower() for word in uncertainty_indicators):
            return 75
        return 85
    
    async def synthesize_speech(
        self,
        text: str,
        language: str = "hi"
    ) -> Dict[str, Any]:
        try:
            # Select voice based on language
            voice_id = {
                "hi": settings.AWS_POLLY_VOICE_ID_HINDI,
                "kn": settings.AWS_POLLY_VOICE_ID_KANNADA,
                "en": "Joanna"
            }.get(language, settings.AWS_POLLY_VOICE_ID_HINDI)
            
            # Select engine
            engine = "standard"
            if language in ["hi", "kn"]:
                engine = "neural"
            
            response = self.polly_client.synthesize_speech(
                Text=text,
                OutputFormat='mp3',
                VoiceId=voice_id,
                Engine=engine,
                LanguageCode=self._get_polly_language_code(language)
            )
            
            # Get audio bytes
            audio_bytes = response['AudioStream'].read()
            
            # Upload to S3 for retrieval
            audio_key = f"audio/{uuid.uuid4()}.mp3"
            self.s3_client.put_object(
                Bucket=settings.AWS_S3_BUCKET,
                Key=audio_key,
                Body=audio_bytes,
                ContentType='audio/mpeg'
            )
            
            # Generate presigned URL
            audio_url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': settings.AWS_S3_BUCKET,
                    'Key': audio_key
                },
                ExpiresIn=3600  # 1 hour
            )
            
            return {
                'audio_url': audio_url,
                'audio_key': audio_key,
                'voice_id': voice_id,
                'language': language,
                'engine': engine
            }
        except Exception as e:
            logger.error(f"Polly error: {str(e)}")
            raise
    
    def _get_content_type(self, file_name: str) -> str:
        types = {
            '.pdf': 'application/pdf',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.tiff': 'image/tiff',
            '.bmp': 'image/bmp'
        }
        ext = file_name[file_name.rfind('.'):].lower()
        return types.get(ext, 'application/octet-stream')
    
    def _get_polly_language_code(self, language: str) -> str:
        codes = {
            "hi": "hi-IN",
            "kn": "kn-IN",
            "en": "en-US"
        }
        return codes.get(language, "hi-IN")


# Global service instance
aws_service = AWSService()


def initialize_services():
    aws_service.initialize_services()
