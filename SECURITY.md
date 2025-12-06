# Security Policy

## Supported Versions

TutorFlow is currently in an early development stage (hackathon/early-stage project). At this time, only the `main` branch is actively maintained and supported.

| Version | Supported          |
| ------- | ------------------ |
| main    | :white_check_mark: |

## Reporting a Vulnerability

We take security vulnerabilities seriously. If you discover a security issue in TutorFlow, please report it responsibly.

### How to Report

**Please do NOT create a public GitHub issue** for security vulnerabilities, as this could expose sensitive information.

Instead, please use one of the following methods:

1. **GitHub Security Advisories (Recommended)**
   - Go to the repository's Security tab
   - Click on "Report a vulnerability"
   - Create a private security advisory
   - This ensures that the issue is handled confidentially

### Information to Include

When reporting a vulnerability, please provide:

- A clear description of the vulnerability
- Steps to reproduce the issue
- The affected version/commit (if applicable)
- Potential impact and severity assessment
- Any suggested fixes or mitigations (if available)
- Your environment details (OS, Python version, Django version, etc.)

## Response Process

- **Acknowledgment**: We will acknowledge receipt of your report within 48 hours
- **Initial Assessment**: We will provide an initial assessment within 5 business days
- **Resolution**: We aim to address security issues promptly, with critical vulnerabilities prioritized
- **Disclosure**: Security issues will be disclosed responsibly after a fix is available, following coordinated disclosure practices

All security-related information will be handled confidentially and will not be shared publicly until a fix is available.

## Security Best Practices

When using TutorFlow:

- **Never commit sensitive data** (API keys, passwords, real student data) to the repository
- **Use environment variables** for configuration (see `docs/DEPLOYMENT.md`)
- **Keep dependencies updated** (Dependabot is configured to help with this)
- **Follow deployment guidelines** in `docs/DEPLOYMENT.md` for production environments
- **Use strong passwords** and enable authentication features as appropriate

## Acknowledgments

We appreciate the security research community's efforts to help keep TutorFlow secure. Responsible disclosure helps protect all users of the application.

