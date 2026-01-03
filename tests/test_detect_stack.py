"""
Tests for detect_stack.py

Tests technology stack detection functionality including framework detection,
cloud provider detection, infrastructure detection, and audit recommendations.
"""

import json
import sys
from pathlib import Path

import pytest

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "skill" / "scripts"))

from detect_stack import (
    detect_node_frameworks,
    detect_python_frameworks,
    detect_ruby_frameworks,
    detect_php_frameworks,
    detect_java_frameworks,
    detect_ios,
    detect_android,
    detect_flutter,
    detect_cloud_provider,
    detect_infrastructure,
    detect_api_type,
    detect_compliance_indicators,
    determine_app_type,
    recommend_audits,
    read_file_safe,
)


class TestReadFileSafe:
    """Tests for safe file reading."""

    def test_read_existing_file(self, temp_dir):
        """Test reading an existing file."""
        test_file = temp_dir / "test.txt"
        test_file.write_text("hello world")
        assert read_file_safe(test_file) == "hello world"

    def test_read_nonexistent_file(self, temp_dir):
        """Test reading a non-existent file returns empty string."""
        nonexistent = temp_dir / "does_not_exist.txt"
        assert read_file_safe(nonexistent) == ""


class TestNodeFrameworkDetection:
    """Tests for Node.js framework detection."""

    def test_detect_react(self, temp_dir):
        """Test React detection."""
        package = temp_dir / "package.json"
        package.write_text('{"dependencies": {"react": "^18.0.0"}}')
        result = detect_node_frameworks(temp_dir)
        assert result["detected"]
        assert "react" in result["frameworks"]

    def test_detect_nextjs(self, temp_dir):
        """Test Next.js detection."""
        package = temp_dir / "package.json"
        package.write_text('{"dependencies": {"next": "^14.0.0"}}')
        result = detect_node_frameworks(temp_dir)
        assert "next.js" in result["frameworks"]

    def test_detect_express(self, temp_dir):
        """Test Express detection."""
        package = temp_dir / "package.json"
        package.write_text('{"dependencies": {"express": "^4.18.0"}}')
        result = detect_node_frameworks(temp_dir)
        assert "express" in result["frameworks"]

    def test_detect_react_native_mobile(self, temp_dir):
        """Test React Native detection sets mobile flag."""
        package = temp_dir / "package.json"
        package.write_text('{"dependencies": {"react-native": "^0.72.0"}}')
        result = detect_node_frameworks(temp_dir)
        assert "react-native" in result["frameworks"]
        assert result["is_mobile"]

    def test_detect_expo_mobile(self, temp_dir):
        """Test Expo detection sets mobile flag."""
        package = temp_dir / "package.json"
        package.write_text('{"dependencies": {"expo": "^49.0.0"}}')
        result = detect_node_frameworks(temp_dir)
        assert "expo" in result["frameworks"]
        assert result["is_mobile"]

    def test_no_package_json(self, temp_dir):
        """Test handling of missing package.json."""
        result = detect_node_frameworks(temp_dir)
        assert not result["detected"]
        assert result["frameworks"] == []

    def test_multiple_frameworks(self, sample_node_project):
        """Test detection of multiple frameworks."""
        result = detect_node_frameworks(sample_node_project)
        assert "react" in result["frameworks"]
        assert "express" in result["frameworks"]


class TestPythonFrameworkDetection:
    """Tests for Python framework detection."""

    def test_detect_django(self, temp_dir):
        """Test Django detection."""
        requirements = temp_dir / "requirements.txt"
        requirements.write_text("django>=4.0\n")
        result = detect_python_frameworks(temp_dir)
        assert result["detected"]
        assert "django" in result["frameworks"]

    def test_detect_fastapi(self, temp_dir):
        """Test FastAPI detection."""
        requirements = temp_dir / "requirements.txt"
        requirements.write_text("fastapi>=0.100.0\n")
        result = detect_python_frameworks(temp_dir)
        assert "fastapi" in result["frameworks"]

    def test_detect_flask(self, temp_dir):
        """Test Flask detection."""
        requirements = temp_dir / "requirements.txt"
        requirements.write_text("Flask>=2.0\n")
        result = detect_python_frameworks(temp_dir)
        assert "flask" in result["frameworks"]

    def test_detect_from_pyproject(self, temp_dir):
        """Test detection from pyproject.toml."""
        pyproject = temp_dir / "pyproject.toml"
        pyproject.write_text('''
[project]
dependencies = ["django>=4.0"]
''')
        result = detect_python_frameworks(temp_dir)
        assert result["detected"]
        assert "django" in result["frameworks"]

    def test_no_python_files(self, temp_dir):
        """Test handling when no Python files exist."""
        result = detect_python_frameworks(temp_dir)
        assert not result["detected"]


class TestRubyFrameworkDetection:
    """Tests for Ruby framework detection."""

    def test_detect_rails(self, temp_dir):
        """Test Rails detection."""
        gemfile = temp_dir / "Gemfile"
        gemfile.write_text("gem 'rails', '~> 7.0'\n")
        result = detect_ruby_frameworks(temp_dir)
        assert result["detected"]
        assert "rails" in result["frameworks"]

    def test_detect_sinatra(self, temp_dir):
        """Test Sinatra detection."""
        gemfile = temp_dir / "Gemfile"
        gemfile.write_text("gem 'sinatra'\n")
        result = detect_ruby_frameworks(temp_dir)
        assert "sinatra" in result["frameworks"]


class TestPHPFrameworkDetection:
    """Tests for PHP framework detection."""

    def test_detect_laravel(self, temp_dir):
        """Test Laravel detection."""
        composer = temp_dir / "composer.json"
        composer.write_text('{"require": {"laravel/framework": "^10.0"}}')
        result = detect_php_frameworks(temp_dir)
        assert result["detected"]
        assert "laravel" in result["frameworks"]

    def test_detect_symfony(self, temp_dir):
        """Test Symfony detection."""
        composer = temp_dir / "composer.json"
        composer.write_text('{"require": {"symfony/framework-bundle": "^6.0"}}')
        result = detect_php_frameworks(temp_dir)
        assert "symfony" in result["frameworks"]


class TestJavaFrameworkDetection:
    """Tests for Java/Kotlin framework detection."""

    def test_detect_spring_boot_maven(self, temp_dir):
        """Test Spring Boot detection from pom.xml."""
        pom = temp_dir / "pom.xml"
        pom.write_text('''
<project>
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter</artifactId>
        </dependency>
    </dependencies>
</project>
''')
        result = detect_java_frameworks(temp_dir)
        assert result["detected"]
        assert "spring-boot" in result["frameworks"]

    def test_detect_spring_boot_gradle(self, temp_dir):
        """Test Spring Boot detection from build.gradle."""
        gradle = temp_dir / "build.gradle"
        gradle.write_text('''
plugins {
    id 'org.springframework.boot' version '3.0.0'
}
''')
        result = detect_java_frameworks(temp_dir)
        assert "spring-boot" in result["frameworks"]


class TestMobilePlatformDetection:
    """Tests for mobile platform detection."""

    def test_detect_ios_podfile(self, temp_dir):
        """Test iOS detection via Podfile."""
        podfile = temp_dir / "Podfile"
        podfile.write_text("platform :ios, '14.0'\n")
        assert detect_ios(temp_dir)

    def test_detect_ios_xcodeproj(self, temp_dir):
        """Test iOS detection via .xcodeproj."""
        xcodeproj = temp_dir / "App.xcodeproj"
        xcodeproj.mkdir()
        assert detect_ios(temp_dir)

    def test_detect_android_manifest(self, temp_dir):
        """Test Android detection via AndroidManifest.xml."""
        android_dir = temp_dir / "app" / "src" / "main"
        android_dir.mkdir(parents=True)
        manifest = android_dir / "AndroidManifest.xml"
        manifest.write_text('<manifest package="com.example.app" />')
        assert detect_android(temp_dir)

    def test_detect_android_gradle(self, temp_dir):
        """Test Android detection via build.gradle."""
        app_dir = temp_dir / "app"
        app_dir.mkdir()
        gradle = app_dir / "build.gradle"
        gradle.write_text('''
android {
    compileSdkVersion 33
}
''')
        assert detect_android(temp_dir)

    def test_detect_flutter(self, temp_dir):
        """Test Flutter detection."""
        pubspec = temp_dir / "pubspec.yaml"
        pubspec.write_text('''
name: my_app
dependencies:
  flutter:
    sdk: flutter
''')
        assert detect_flutter(temp_dir)


class TestCloudProviderDetection:
    """Tests for cloud provider detection."""

    def test_detect_aws_terraform(self, aws_project):
        """Test AWS detection from Terraform."""
        assert detect_cloud_provider(aws_project) == "aws"

    def test_detect_gcp_terraform(self, temp_dir):
        """Test GCP detection from Terraform."""
        tf = temp_dir / "main.tf"
        tf.write_text('provider "google" { project = "my-project" }')
        assert detect_cloud_provider(temp_dir) == "gcp"

    def test_detect_azure_terraform(self, temp_dir):
        """Test Azure detection from Terraform."""
        tf = temp_dir / "main.tf"
        tf.write_text('provider "azurerm" { features {} }')
        assert detect_cloud_provider(temp_dir) == "azure"

    def test_detect_aws_serverless(self, temp_dir):
        """Test AWS detection from serverless.yml."""
        serverless = temp_dir / "serverless.yml"
        serverless.write_text('''
service: my-service
provider:
  name: aws
  runtime: nodejs18.x
''')
        assert detect_cloud_provider(temp_dir) == "aws"


class TestInfrastructureDetection:
    """Tests for infrastructure technology detection."""

    def test_detect_docker(self, temp_dir):
        """Test Docker detection."""
        dockerfile = temp_dir / "Dockerfile"
        dockerfile.write_text("FROM node:18\n")
        infra = detect_infrastructure(temp_dir)
        assert "docker" in infra

    def test_detect_docker_compose(self, temp_dir):
        """Test docker-compose detection."""
        compose = temp_dir / "docker-compose.yml"
        compose.write_text("version: '3'\nservices:\n  web:\n    image: nginx\n")
        infra = detect_infrastructure(temp_dir)
        assert "docker" in infra

    def test_detect_kubernetes(self, kubernetes_project):
        """Test Kubernetes detection."""
        infra = detect_infrastructure(kubernetes_project)
        assert "kubernetes" in infra

    def test_detect_terraform(self, aws_project):
        """Test Terraform detection."""
        infra = detect_infrastructure(aws_project)
        assert "terraform" in infra

    def test_detect_serverless(self, temp_dir):
        """Test Serverless Framework detection."""
        serverless = temp_dir / "serverless.yml"
        serverless.write_text("service: my-service\n")
        infra = detect_infrastructure(temp_dir)
        assert "serverless" in infra


class TestAPITypeDetection:
    """Tests for API type detection."""

    def test_detect_graphql_schema(self, temp_dir):
        """Test GraphQL detection from schema file."""
        schema = temp_dir / "schema.graphql"
        schema.write_text("type Query { hello: String }")
        api_types = detect_api_type(temp_dir)
        assert "graphql" in api_types

    def test_detect_grpc(self, temp_dir):
        """Test gRPC detection."""
        proto = temp_dir / "service.proto"
        proto.write_text("syntax = \"proto3\";")
        api_types = detect_api_type(temp_dir)
        assert "grpc" in api_types

    def test_rest_default(self, temp_dir):
        """Test that REST is always included."""
        api_types = detect_api_type(temp_dir)
        assert "rest" in api_types


class TestComplianceDetection:
    """Tests for compliance indicator detection."""

    def test_detect_hipaa(self, temp_dir):
        """Test HIPAA detection."""
        readme = temp_dir / "README.md"
        readme.write_text("This application is HIPAA compliant and handles PHI.")
        indicators = detect_compliance_indicators(temp_dir)
        assert "hipaa" in indicators

    def test_detect_pci_dss(self, temp_dir):
        """Test PCI-DSS detection."""
        readme = temp_dir / "README.md"
        readme.write_text("PCI-DSS compliant payment processing.")
        indicators = detect_compliance_indicators(temp_dir)
        assert "pci-dss" in indicators

    def test_detect_gdpr(self, temp_dir):
        """Test GDPR detection."""
        readme = temp_dir / "README.md"
        readme.write_text("GDPR compliant data handling.")
        indicators = detect_compliance_indicators(temp_dir)
        assert "gdpr" in indicators

    def test_detect_soc2(self, temp_dir):
        """Test SOC 2 detection."""
        readme = temp_dir / "README.md"
        readme.write_text("SOC 2 Type II certified.")
        indicators = detect_compliance_indicators(temp_dir)
        assert "soc2" in indicators


class TestAppTypeDetermination:
    """Tests for application type determination."""

    def test_mobile_app(self):
        """Test mobile app type."""
        assert determine_app_type(["ios", "android"], []) == "mobile"

    def test_full_stack_mobile_web(self):
        """Test full-stack with mobile and web."""
        assert determine_app_type(["web", "ios"], ["react"]) == "full-stack"

    def test_api_only(self):
        """Test API-only app."""
        assert determine_app_type(["web"], ["express"]) == "api"

    def test_full_stack_web(self):
        """Test full-stack web app."""
        assert determine_app_type(["web"], ["react", "express"]) == "full-stack"

    def test_web_frontend(self):
        """Test web frontend only."""
        assert determine_app_type(["web"], ["react"]) == "web"


class TestAuditRecommendations:
    """Tests for audit recommendation generation."""

    def test_mobile_recommendation(self):
        """Test mobile audit recommendation."""
        detection = {
            "platforms": ["ios", "android"],
            "cloud": "unknown",
            "infrastructure": [],
            "api_type": ["rest"],
        }
        recs = recommend_audits(detection)
        assert "mobile" in recs["recommended_specialized"]

    def test_aws_recommendation(self):
        """Test AWS audit recommendation."""
        detection = {
            "platforms": ["web"],
            "cloud": "aws",
            "infrastructure": [],
            "api_type": ["rest"],
        }
        recs = recommend_audits(detection)
        assert "aws" in recs["recommended_specialized"]

    def test_kubernetes_recommendation(self):
        """Test Kubernetes audit recommendation."""
        detection = {
            "platforms": ["web"],
            "cloud": "unknown",
            "infrastructure": ["kubernetes"],
            "api_type": ["rest"],
        }
        recs = recommend_audits(detection)
        assert "kubernetes" in recs["recommended_specialized"]

    def test_graphql_recommendation(self):
        """Test GraphQL audit recommendation."""
        detection = {
            "platforms": ["web"],
            "cloud": "unknown",
            "infrastructure": [],
            "api_type": ["graphql", "rest"],
        }
        recs = recommend_audits(detection)
        assert "graphql" in recs["recommended_specialized"]

    def test_all_phases_recommended(self):
        """Test that all 13 core phases are recommended."""
        detection = {
            "platforms": ["web"],
            "cloud": "unknown",
            "infrastructure": [],
            "api_type": ["rest"],
        }
        recs = recommend_audits(detection)
        assert recs["recommended_phases"] == list(range(13))
