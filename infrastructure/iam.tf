# Define the IAM role
resource "aws_iam_role" "ec2_access_role" {
  name = "EC2HelfulAIAccessRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Principal = {
          Service = "ec2.amazonaws.com" # Assuming the role is for EC2 instances
        },
        Effect = "Allow",
        Sid    = ""
      }
    ]
  })
}


resource "aws_iam_policy" "ec2_access_policy" {
  name        = "HelpfulAIAccessPolicy"
  description = "My policy that grants access to Helpful AI services"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action   = "s3:*",
        Effect   = "Allow",
        Resource = "*" # Grants all actions on all S3 resources
      },
      {
        Action = [
          "secretsmanager:GetSecretValue",
          "secretsmanager:DescribeSecret"
        ],
        Effect   = "Allow",
        Resource = "*" # Specify the ARN of the secrets if you want to restrict access
      }
    ]
  })
}


# Attach the policy to the role
resource "aws_iam_role_policy_attachment" "ec2_attach" {
  policy_arn = aws_iam_policy.ec2_access_policy.arn
  role       = aws_iam_role.ec2_access_role.name
}

# Create the EC2 instance profile
resource "aws_iam_instance_profile" "ec2_instance_profile" {
  name = "HelpfulAIInstanceProfile"
  role = aws_iam_role.ec2_access_role.name
}