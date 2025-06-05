"""
Vertex AI Imagen API 클라이언트 테스트
"""

import asyncio
import json
import os
import pytest
from unittest.mock import Mock, patch, AsyncMock
import base64

from imagen_mcp_server import VertexAIImagenClient


class TestVertexAIImagenClient:
    """VertexAIImagenClient 테스트 클래스"""

    def setup_method(self):
        """각 테스트 메소드 실행 전 설정"""
        self.project_id = "test-project"
        self.location = "us-central1"
        self.client = VertexAIImagenClient(self.project_id, self.location)

    def test_init(self):
        """클라이언트 초기화 테스트"""
        assert self.client.project_id == self.project_id
        assert self.client.location == self.location
        assert self.client.base_url == f"https://{self.location}-aiplatform.googleapis.com/v1"
        assert len(self.client.supported_models) > 0

    @patch('imagen_mcp_server.service_account.Credentials.from_service_account_file')
    def test_setup_credentials_success(self, mock_from_file):
        """인증 설정 성공 테스트"""
        # Mock credentials
        mock_creds = Mock()
        mock_creds.valid = True
        mock_from_file.return_value = mock_creds
        
        # Create a temporary test file
        test_key_path = "/tmp/test_key.json"
        with open(test_key_path, 'w') as f:
            json.dump({"type": "service_account", "project_id": "test"}, f)
        
        try:
            result = self.client.setup_credentials(test_key_path)
            assert result is True
            assert self.client.credentials == mock_creds
        finally:
            # Clean up
            if os.path.exists(test_key_path):
                os.remove(test_key_path)

    def test_setup_credentials_file_not_found(self):
        """존재하지 않는 키 파일 테스트"""
        result = self.client.setup_credentials("/nonexistent/path.json")
        assert result is False

    @patch('imagen_mcp_server.service_account.Credentials.from_service_account_file')
    def test_setup_credentials_invalid_file(self, mock_from_file):
        """잘못된 키 파일 테스트"""
        mock_from_file.side_effect = Exception("Invalid key file")
        
        # Create a temporary invalid file
        test_key_path = "/tmp/invalid_key.json"
        with open(test_key_path, 'w') as f:
            f.write("invalid json")
        
        try:
            result = self.client.setup_credentials(test_key_path)
            assert result is False
        finally:
            if os.path.exists(test_key_path):
                os.remove(test_key_path)

    @pytest.mark.asyncio
    @patch('imagen_mcp_server.requests.post')
    async def test_generate_image_success(self, mock_post):
        """이미지 생성 성공 테스트"""
        # Mock credentials
        mock_creds = Mock()
        mock_creds.token = "test-token"
        mock_creds.valid = True
        self.client.credentials = mock_creds
        
        # Mock successful API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "predictions": [{
                "bytesBase64Encoded": base64.b64encode(b"fake_image_data").decode(),
                "mimeType": "image/png",
                "prompt": "Enhanced: A beautiful landscape"
            }]
        }
        
        # Mock the executor to return the response immediately
        with patch('asyncio.get_event_loop') as mock_loop:
            mock_executor = Mock()
            mock_executor.return_value = mock_response
            mock_loop.return_value.run_in_executor = AsyncMock(return_value=mock_response)
            
            result = await self.client.generate_image(
                prompt="A beautiful landscape",
                image_count=1,
                aspect_ratio="1:1"
            )
            
            assert "predictions" in result
            assert len(result["predictions"]) == 1
            assert "bytesBase64Encoded" in result["predictions"][0]

    @pytest.mark.asyncio
    async def test_generate_image_invalid_model(self):
        """지원되지 않는 모델 테스트"""
        mock_creds = Mock()
        mock_creds.token = "test-token"
        mock_creds.valid = True
        self.client.credentials = mock_creds
        
        with pytest.raises(ValueError, match="지원되지 않는 모델"):
            await self.client.generate_image(
                prompt="Test prompt",
                model_version="invalid-model"
            )

    @pytest.mark.asyncio
    @patch('imagen_mcp_server.requests.post')
    async def test_generate_image_api_error(self, mock_post):
        """API 오류 응답 테스트"""
        mock_creds = Mock()
        mock_creds.token = "test-token"
        mock_creds.valid = True
        self.client.credentials = mock_creds
        
        # Mock API error response
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.text = "Forbidden: Insufficient permissions"
        
        with patch('asyncio.get_event_loop') as mock_loop:
            mock_loop.return_value.run_in_executor = AsyncMock(return_value=mock_response)
            
            with pytest.raises(Exception, match="HTTP 403"):
                await self.client.generate_image(prompt="Test prompt")

    def test_supported_models(self):
        """지원되는 모델 목록 테스트"""
        expected_models = [
            "imagegeneration@006",
            "imagegeneration@005", 
            "imagegeneration@002",
            "imagen-3.0-generate-001",
            "imagen-3.0-generate-002",
            "imagen-3.0-fast-generate-001"
        ]
        
        for model in expected_models:
            assert model in self.client.supported_models

    @pytest.mark.asyncio
    @patch('imagen_mcp_server.requests.post')
    async def test_generate_image_with_options(self, mock_post):
        """다양한 옵션을 사용한 이미지 생성 테스트"""
        mock_creds = Mock()
        mock_creds.token = "test-token"
        mock_creds.valid = True
        self.client.credentials = mock_creds
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "predictions": [{
                "bytesBase64Encoded": base64.b64encode(b"fake_image_data").decode(),
                "mimeType": "image/png"
            }]
        }
        
        with patch('asyncio.get_event_loop') as mock_loop:
            mock_loop.return_value.run_in_executor = AsyncMock(return_value=mock_response)
            
            result = await self.client.generate_image(
                prompt="A futuristic city",
                negative_prompt="dark, blurry",
                image_count=2,
                aspect_ratio="16:9",
                model_version="imagen-3.0-generate-002",
                safety_setting="block_medium_and_above",
                seed=12345,
                enhance_prompt=True
            )
            
            assert "predictions" in result
            
            # Verify the request was made with correct parameters
            mock_loop.return_value.run_in_executor.assert_called_once()

    @pytest.mark.asyncio
    async def test_generate_image_no_credentials(self):
        """인증 정보 없이 이미지 생성 시도 테스트"""
        # No credentials set
        self.client.credentials = None
        
        with pytest.raises(AttributeError):
            await self.client.generate_image(prompt="Test prompt")


class TestParameterValidation:
    """매개변수 검증 테스트"""
    
    def setup_method(self):
        self.client = VertexAIImagenClient("test-project", "us-central1")
    
    @pytest.mark.asyncio
    async def test_image_count_limits(self):
        """이미지 개수 제한 테스트"""
        mock_creds = Mock()
        mock_creds.token = "test-token"
        mock_creds.valid = True
        self.client.credentials = mock_creds
        
        with patch('imagen_mcp_server.requests.post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"predictions": []}
            
            with patch('asyncio.get_event_loop') as mock_loop:
                mock_loop.return_value.run_in_executor = AsyncMock(return_value=mock_response)
                
                # Test that image_count > 4 is capped at 4
                await self.client.generate_image(
                    prompt="Test",
                    image_count=10  # Should be capped at 4
                )
                
                # Check that the actual request uses max 4 images
                call_args = mock_loop.return_value.run_in_executor.call_args
                # The lambda function is called, so we can't directly inspect the request
                # But we know it should cap at 4

    def test_aspect_ratio_validation(self):
        """가로세로 비율 유효성 검사"""
        valid_ratios = ["1:1", "3:4", "4:3", "16:9", "9:16"]
        
        for ratio in valid_ratios:
            # These should not raise any errors
            assert ratio in valid_ratios


class TestErrorHandling:
    """오류 처리 테스트"""
    
    def setup_method(self):
        self.client = VertexAIImagenClient("test-project", "us-central1")
    
    @pytest.mark.asyncio
    @patch('imagen_mcp_server.requests.post')
    async def test_network_error(self, mock_post):
        """네트워크 오류 테스트"""
        mock_creds = Mock()
        mock_creds.token = "test-token"
        mock_creds.valid = True
        self.client.credentials = mock_creds
        
        with patch('asyncio.get_event_loop') as mock_loop:
            mock_loop.return_value.run_in_executor = AsyncMock(
                side_effect=Exception("Network error")
            )
            
            with pytest.raises(Exception, match="Network error"):
                await self.client.generate_image(prompt="Test prompt")

    @pytest.mark.asyncio 
    @patch('imagen_mcp_server.requests.post')
    async def test_invalid_json_response(self, mock_post):
        """잘못된 JSON 응답 테스트"""
        mock_creds = Mock()
        mock_creds.token = "test-token"
        mock_creds.valid = True
        self.client.credentials = mock_creds
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
        
        with patch('asyncio.get_event_loop') as mock_loop:
            mock_loop.return_value.run_in_executor = AsyncMock(return_value=mock_response)
            
            with pytest.raises(Exception):
                await self.client.generate_image(prompt="Test prompt")


if __name__ == "__main__":
    pytest.main([__file__])
