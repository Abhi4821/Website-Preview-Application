provider "aws" {
  region  = "ap-south-1"
  profile = "website-preview-prod"

  default_tags {
    tags = {
      Project     = "WebsitePreview"
      Environment = "Production"
      ManagedBy   = "Terraform"
    }
  }
}
