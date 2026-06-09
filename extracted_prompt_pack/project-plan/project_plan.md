# Healthcare Appointment Platform

## Summary
This project aims to develop a comprehensive healthcare appointment platform designed to serve patients, doctors, and administrative staff. The platform will streamline the appointment scheduling process, improve communication, and enhance overall workflow efficiency within a healthcare setting. Given the healthcare domain, significant attention will be paid to privacy, compliance, and security.

- Domain: healthcare
- Project type: healthcare workflow improvement
- Complexity: medium
- Status: plan_generated

## Warnings
- Healthcare workflows may require privacy, compliance, and security review.

## Phases
### P1: Discovery & Planning
To gather detailed requirements, define the project scope, and establish the foundational technical and compliance architecture.

Estimated duration: 4-6 weeks

Tasks:
- T1.1: Stakeholder Interviews & Requirements Gathering - Conduct interviews with patients, doctors, and administrative staff to understand current pain points, desired features, and workflow needs.
- T1.2: Technical Architecture Design - Design the high-level technical architecture, including technology stack, database schema, and API structure. Dependencies: T1.1.
- T1.3: Compliance & Security Review - Identify and document all relevant healthcare regulations (e.g., HIPAA, GDPR) and define security protocols for data handling and platform access. Dependencies: T1.1.

Deliverables:
- Project Scope Document
- Detailed Requirements Document (DRD)
- Technical Design Document (TDD)
- Compliance & Security Plan

### P2: Design & Prototyping
To create intuitive and user-friendly interfaces for all user roles and validate design concepts with stakeholders.

Estimated duration: 5-7 weeks

Tasks:
- T2.1: User Persona & Journey Mapping - Develop detailed user personas for patients, doctors, and admins, and map their typical journeys through the platform. Dependencies: T1.1.
- T2.2: Wireframing & Low-Fidelity Prototyping - Create wireframes and low-fidelity prototypes for key screens and workflows. Dependencies: T2.1.
- T2.3: UI/UX Design & High-Fidelity Prototyping - Develop the visual design (UI) and create high-fidelity interactive prototypes for patient, doctor, and admin portals. Dependencies: T2.2.
- T2.4: Design Review & User Feedback - Conduct internal and external reviews of the prototypes to gather feedback and iterate on designs. Dependencies: T2.3.

Deliverables:
- User Personas & Journey Maps
- Wireframes
- UI Mockups
- Interactive High-Fidelity Prototypes
- Design System/Style Guide

### P3: Development
To build the backend infrastructure, APIs, and frontend user interfaces for all platform components.

Estimated duration: 12-16 weeks

Tasks:
- T3.1: Database Development - Implement the database schema based on the technical design, including tables, relationships, and indexing. Dependencies: T1.2.
- T3.2: Backend API Development - Develop the core backend APIs for user authentication, appointment management, patient records, notifications, etc. Dependencies: T3.1.
- T3.3: Patient Portal Development - Build the frontend interface for patients to schedule, view, and manage appointments, and access their information. Dependencies: T2.3, T3.2.
- T3.4: Doctor Portal Development - Build the frontend interface for doctors to view schedules, manage appointments, and access patient details. Dependencies: T2.3, T3.2.
- T3.5: Admin Portal Development - Build the frontend interface for administrators to manage users, schedules, settings, and generate reports. Dependencies: T2.3, T3.2.
- T3.6: Integration Development (Optional) - Develop integrations with existing EHR/EMR systems or other third-party services (e.g., payment gateways, telehealth platforms). Dependencies: T3.2, T1.2.

Deliverables:
- Functional Backend APIs
- Patient Portal (Frontend)
- Doctor Portal (Frontend)
- Admin Portal (Frontend)
- Integrated Modules (if applicable)

### P4: Testing & Quality Assurance
To ensure the platform is robust, secure, compliant, and meets all functional and non-functional requirements.

Estimated duration: 6-8 weeks

Tasks:
- T4.1: Unit & Integration Testing - Perform unit tests on individual code components and integration tests on modules and API interactions. Dependencies: P3.
- T4.2: System & End-to-End Testing - Conduct comprehensive system testing to verify all functionalities across the entire platform and end-to-end user flows. Dependencies: T4.1.
- T4.3: Security & Performance Testing - Perform penetration testing, vulnerability assessments, and load/stress testing to ensure platform security and performance under expected loads. Dependencies: T4.2, T1.3.
- T4.4: User Acceptance Testing (UAT) - Engage key stakeholders (patients, doctors, admins) to test the platform in a simulated environment and provide final approval. Dependencies: T4.3.
- T4.5: Bug Fixing & Regression Testing - Address all identified bugs and perform regression testing to ensure fixes haven't introduced new issues. Dependencies: T4.1, T4.2, T4.3, T4.4.

Deliverables:
- Test Plans & Reports
- Security Audit Report
- Performance Test Report
- UAT Sign-off Document
- Resolved Bug List

### P5: Deployment & Launch
To successfully deploy the platform to the production environment and make it available to end-users.

Estimated duration: 2-3 weeks

Tasks:
- T5.1: Infrastructure Setup & Configuration - Provision and configure production servers, databases, and network infrastructure. Dependencies: T1.2, T4.5.
- T5.2: Deployment to Production - Deploy the tested and approved application code to the production environment. Dependencies: T5.1.
- T5.3: Data Migration (if applicable) - Migrate existing patient, doctor, or appointment data into the new platform. Dependencies: T5.2.
- T5.4: User Training & Onboarding - Provide training sessions and documentation for doctors, admins, and potentially patients on how to use the new platform. Dependencies: T4.4.
- T5.5: Go-Live & Monitoring Setup - Officially launch the platform and set up continuous monitoring for performance, errors, and security. Dependencies: T5.2, T5.3, T5.4.

Deliverables:
- Deployed Production Platform
- User Training Materials
- Launch Announcement
- Monitoring Dashboards

### P6: Post-Launch Support & Iteration
To provide ongoing support, address issues, gather feedback, and plan for future enhancements.

Estimated duration: Ongoing

Tasks:
- T6.1: Continuous Monitoring & Incident Response - Monitor platform health, performance, and security, and respond to any incidents or outages. Dependencies: T5.5.
- T6.2: Bug Fixes & Minor Enhancements - Address any post-launch bugs and implement small, immediate improvements based on user feedback. Dependencies: T6.1.
- T6.3: Feedback Collection & Analysis - Establish channels for user feedback (e.g., surveys, support tickets) and regularly analyze it for insights. Dependencies: T5.5.
- T6.4: Feature Backlog & Roadmap Planning - Based on feedback and strategic goals, maintain a backlog of new features and plan future development iterations. Dependencies: T6.3.

Deliverables:
- Monitoring Reports
- Resolved Bug Reports
- User Feedback Summaries
- Feature Backlog
- Product Roadmap

## Milestones
- M1: Requirements & Architecture Approved (P1)
- M2: Design Prototype Approved (P2)
- M3: Core Development Complete (P3)
- M4: UAT Sign-off (P4)
- M5: Platform Launched (P5)

## Risks
- R1: Failure to comply with healthcare data privacy regulations (e.g., HIPAA, GDPR). Mitigation: Involve compliance officers early and continuously. Conduct regular security audits and privacy impact assessments. Implement robust data encryption and access controls.
- R2: Difficulty integrating with existing Electronic Health Record (EHR) or Electronic Medical Record (EMR) systems. Mitigation: Conduct thorough discovery of existing systems' APIs/integration capabilities. Prioritize standard integration protocols (e.g., HL7, FHIR). Consider a phased integration approach or an MVP without deep EHR integration initially.
- R3: Low user adoption by patients, doctors, or administrative staff. Mitigation: Involve users in design and testing phases (UAT). Provide comprehensive training and clear onboarding materials. Offer ongoing support and gather feedback for continuous improvement. Highlight clear benefits to users.
- R4: Scope creep due to evolving requirements or new feature requests during development. Mitigation: Establish a clear Minimum Viable Product (MVP) scope. Implement a strict change management process. Prioritize features based on business value and feasibility. Communicate scope changes and their impact clearly.
- R5: Security breaches or data loss due to vulnerabilities in the platform. Mitigation: Implement security best practices throughout the SDLC (Secure by Design). Conduct regular penetration testing and vulnerability assessments. Use secure coding guidelines. Implement robust logging and monitoring.

## Recommendations
- Compliance & Security: Appoint a dedicated compliance and security lead for the project.
- Development Strategy: Adopt an Agile development methodology with iterative releases.
- User Engagement: Establish a 'Champion User' program for early adopters among doctors and admins.
- Scalability: Design the platform with cloud-native principles for scalability and resilience.

## Assumptions
- Key stakeholders (patients, doctors, administrative staff) will be available for interviews, feedback, and User Acceptance Testing (UAT) as needed.
- Necessary infrastructure (cloud accounts, development environments) will be provisioned and accessible in a timely manner.
- A clear Minimum Viable Product (MVP) scope will be agreed upon before the development phase begins to manage expectations and control scope.
- Budget and resources (development team, QA, UX, DevOps) are sufficient for a 'medium' complexity project as outlined.
- Existing healthcare systems (if any) have documented APIs or clear data export capabilities for potential integration or migration.

## Engineering Prompt Pack
### Frontend Engineer implementation prompt

**Target Role:** Frontend Engineer  
**Target Tool:** Codex, Cursor, Claude Code, Claude, GitHub Copilot, Lovable, or Bolt  
**Purpose:** Implement the frontend experience for the planned project while preserving the validated project scope.

**Related Phases:**
- P1
- P2
- P3
- P4
- P5
- P6

**Constraints:**
- Use the generated project plan as the source of truth.
- Do not build, deploy, or modify software from inside the planner.
- Keep implementation guidance appropriate for Codex, Cursor, Claude Code, Claude, GitHub Copilot, Lovable, or Bolt.
- Key stakeholders (patients, doctors, administrative staff) will be available for interviews, feedback, and User Acceptance Testing (UAT) as needed.
- Necessary infrastructure (cloud accounts, development environments) will be provisioned and accessible in a timely manner.
- A clear Minimum Viable Product (MVP) scope will be agreed upon before the development phase begins to manage expectations and control scope.
- Budget and resources (development team, QA, UX, DevOps) are sufficient for a 'medium' complexity project as outlined.
- Existing healthcare systems (if any) have documented APIs or clear data export capabilities for potential integration or migration.
- Healthcare workflows may require privacy, compliance, and security review.

**Acceptance Criteria:**
- The Frontend Engineer output is aligned with the validated project plan.
- Relevant phases, tasks, assumptions, risks, and recommendations are addressed.
- The output is structured for engineer review before use in an external AI coding tool.
- Comprehensive list of functional and non-functional requirements documented.
- User stories and use cases defined for each user type.
- Technical Design Document (TDD) approved.

**Prompt:**
```text
You are a senior frontend engineer responsible for implementing the user-facing experience.

## Project Context
Project name: Healthcare Appointment Platform
Project description: Build a healthcare appointment platform for patients, doctors, and admins
Domain: healthcare
Project type: healthcare workflow improvement
Complexity: medium
Summary: This project aims to develop a comprehensive healthcare appointment platform designed to serve patients, doctors, and administrative staff. The platform will streamline the appointment scheduling process, improve communication, and enhance overall workflow efficiency within a healthcare setting. Given the healthcare domain, significant attention will be paid to privacy, compliance, and security.

## Your Role
Frontend Engineer

## Goal
Implement the frontend experience for the planned project while preserving the validated project scope.

## Technical Scope
UI workflows, client-side validation, accessibility, responsive behavior, and integration points with backend APIs.

Relevant tasks:
- T1.1: Stakeholder Interviews & Requirements Gathering - Conduct interviews with patients, doctors, and administrative staff to understand current pain points, desired features, and workflow needs.
- T1.2: Technical Architecture Design - Design the high-level technical architecture, including technology stack, database schema, and API structure.
- T1.3: Compliance & Security Review - Identify and document all relevant healthcare regulations (e.g., HIPAA, GDPR) and define security protocols for data handling and platform access.
- T2.1: User Persona & Journey Mapping - Develop detailed user personas for patients, doctors, and admins, and map their typical journeys through the platform.
- T2.2: Wireframing & Low-Fidelity Prototyping - Create wireframes and low-fidelity prototypes for key screens and workflows.
- T2.3: UI/UX Design & High-Fidelity Prototyping - Develop the visual design (UI) and create high-fidelity interactive prototypes for patient, doctor, and admin portals.
- T2.4: Design Review & User Feedback - Conduct internal and external reviews of the prototypes to gather feedback and iterate on designs.
- T3.1: Database Development - Implement the database schema based on the technical design, including tables, relationships, and indexing.
- T3.2: Backend API Development - Develop the core backend APIs for user authentication, appointment management, patient records, notifications, etc.
- T3.3: Patient Portal Development - Build the frontend interface for patients to schedule, view, and manage appointments, and access their information.
- T3.4: Doctor Portal Development - Build the frontend interface for doctors to view schedules, manage appointments, and access patient details.
- T3.5: Admin Portal Development - Build the frontend interface for administrators to manage users, schedules, settings, and generate reports.
- T3.6: Integration Development (Optional) - Develop integrations with existing EHR/EMR systems or other third-party services (e.g., payment gateways, telehealth platforms).
- T4.1: Unit & Integration Testing - Perform unit tests on individual code components and integration tests on modules and API interactions.
- T4.2: System & End-to-End Testing - Conduct comprehensive system testing to verify all functionalities across the entire platform and end-to-end user flows.
- T4.3: Security & Performance Testing - Perform penetration testing, vulnerability assessments, and load/stress testing to ensure platform security and performance under expected loads.
- T4.4: User Acceptance Testing (UAT) - Engage key stakeholders (patients, doctors, admins) to test the platform in a simulated environment and provide final approval.
- T4.5: Bug Fixing & Regression Testing - Address all identified bugs and perform regression testing to ensure fixes haven't introduced new issues.
- T5.1: Infrastructure Setup & Configuration - Provision and configure production servers, databases, and network infrastructure.
- T5.2: Deployment to Production - Deploy the tested and approved application code to the production environment.
- T5.3: Data Migration (if applicable) - Migrate existing patient, doctor, or appointment data into the new platform.
- T5.4: User Training & Onboarding - Provide training sessions and documentation for doctors, admins, and potentially patients on how to use the new platform.
- T5.5: Go-Live & Monitoring Setup - Officially launch the platform and set up continuous monitoring for performance, errors, and security.
- T6.1: Continuous Monitoring & Incident Response - Monitor platform health, performance, and security, and respond to any incidents or outages.
- T6.2: Bug Fixes & Minor Enhancements - Address any post-launch bugs and implement small, immediate improvements based on user feedback.
- T6.3: Feedback Collection & Analysis - Establish channels for user feedback (e.g., surveys, support tickets) and regularly analyze it for insights.
- T6.4: Feature Backlog & Roadmap Planning - Based on feedback and strategic goals, maintain a backlog of new features and plan future development iterations.

Risks to account for:
- Failure to comply with healthcare data privacy regulations (e.g., HIPAA, GDPR).
- Difficulty integrating with existing Electronic Health Record (EHR) or Electronic Medical Record (EMR) systems.
- Low user adoption by patients, doctors, or administrative staff.
- Scope creep due to evolving requirements or new feature requests during development.
- Security breaches or data loss due to vulnerabilities in the platform.

Recommendations to preserve:
- Appoint a dedicated compliance and security lead for the project.
- Adopt an Agile development methodology with iterative releases.
- Establish a 'Champion User' program for early adopters among doctors and admins.
- Design the platform with cloud-native principles for scalability and resilience.

Assumptions to keep visible:
- Key stakeholders (patients, doctors, administrative staff) will be available for interviews, feedback, and User Acceptance Testing (UAT) as needed.
- Necessary infrastructure (cloud accounts, development environments) will be provisioned and accessible in a timely manner.
- A clear Minimum Viable Product (MVP) scope will be agreed upon before the development phase begins to manage expectations and control scope.
- Budget and resources (development team, QA, UX, DevOps) are sufficient for a 'medium' complexity project as outlined.
- Existing healthcare systems (if any) have documented APIs or clear data export capabilities for potential integration or migration.

## Related Phases
- P1: Discovery & Planning (4-6 weeks) - To gather detailed requirements, define the project scope, and establish the foundational technical and compliance architecture.
- P2: Design & Prototyping (5-7 weeks) - To create intuitive and user-friendly interfaces for all user roles and validate design concepts with stakeholders.
- P3: Development (12-16 weeks) - To build the backend infrastructure, APIs, and frontend user interfaces for all platform components.
- P4: Testing & Quality Assurance (6-8 weeks) - To ensure the platform is robust, secure, compliant, and meets all functional and non-functional requirements.
- P5: Deployment & Launch (2-3 weeks) - To successfully deploy the platform to the production environment and make it available to end-users.
- P6: Post-Launch Support & Iteration (Ongoing) - To provide ongoing support, address issues, gather feedback, and plan for future enhancements.

## Constraints
- Use the generated project plan as the source of truth.
- Do not build, deploy, or modify software from inside the planner.
- Keep implementation guidance appropriate for Codex, Cursor, Claude Code, Claude, GitHub Copilot, Lovable, or Bolt.
- Key stakeholders (patients, doctors, administrative staff) will be available for interviews, feedback, and User Acceptance Testing (UAT) as needed.
- Necessary infrastructure (cloud accounts, development environments) will be provisioned and accessible in a timely manner.
- A clear Minimum Viable Product (MVP) scope will be agreed upon before the development phase begins to manage expectations and control scope.
- Budget and resources (development team, QA, UX, DevOps) are sufficient for a 'medium' complexity project as outlined.
- Existing healthcare systems (if any) have documented APIs or clear data export capabilities for potential integration or migration.
- Healthcare workflows may require privacy, compliance, and security review.

## Expected Output
Produce implementation guidance or artifacts for Codex, Cursor, Claude Code, Claude, GitHub Copilot, Lovable, or Bolt. The output should be ready for an engineer to review and apply externally.
The planner itself must not build, deploy, or modify software.

## Acceptance Criteria
- The Frontend Engineer output is aligned with the validated project plan.
- Relevant phases, tasks, assumptions, risks, and recommendations are addressed.
- The output is structured for engineer review before use in an external AI coding tool.
- Comprehensive list of functional and non-functional requirements documented.
- User stories and use cases defined for each user type.
- Technical Design Document (TDD) approved.

## Do Not Do
- Do not build or deploy the application automatically.
- Do not invent requirements, credentials, budgets, deadlines, integrations, or production infrastructure.
- Do not remove assumptions, warnings, risks, or acceptance criteria from the engineering handoff.
- Do not treat this prompt as a substitute for engineer review.
```

### Backend Engineer implementation prompt

**Target Role:** Backend Engineer  
**Target Tool:** Codex, Cursor, Claude Code, Claude, GitHub Copilot, Lovable, or Bolt  
**Purpose:** Implement backend services that support the planned workflows, validation rules, and task sequencing.

**Related Phases:**
- P1
- P2
- P3
- P4
- P5
- P6

**Constraints:**
- Use the generated project plan as the source of truth.
- Do not build, deploy, or modify software from inside the planner.
- Keep implementation guidance appropriate for Codex, Cursor, Claude Code, Claude, GitHub Copilot, Lovable, or Bolt.
- Key stakeholders (patients, doctors, administrative staff) will be available for interviews, feedback, and User Acceptance Testing (UAT) as needed.
- Necessary infrastructure (cloud accounts, development environments) will be provisioned and accessible in a timely manner.
- A clear Minimum Viable Product (MVP) scope will be agreed upon before the development phase begins to manage expectations and control scope.
- Budget and resources (development team, QA, UX, DevOps) are sufficient for a 'medium' complexity project as outlined.
- Existing healthcare systems (if any) have documented APIs or clear data export capabilities for potential integration or migration.
- Healthcare workflows may require privacy, compliance, and security review.

**Acceptance Criteria:**
- The Backend Engineer output is aligned with the validated project plan.
- Relevant phases, tasks, assumptions, risks, and recommendations are addressed.
- The output is structured for engineer review before use in an external AI coding tool.
- Comprehensive list of functional and non-functional requirements documented.
- User stories and use cases defined for each user type.
- Technical Design Document (TDD) approved.

**Prompt:**
```text
You are a senior backend engineer responsible for building the application services and API layer.

## Project Context
Project name: Healthcare Appointment Platform
Project description: Build a healthcare appointment platform for patients, doctors, and admins
Domain: healthcare
Project type: healthcare workflow improvement
Complexity: medium
Summary: This project aims to develop a comprehensive healthcare appointment platform designed to serve patients, doctors, and administrative staff. The platform will streamline the appointment scheduling process, improve communication, and enhance overall workflow efficiency within a healthcare setting. Given the healthcare domain, significant attention will be paid to privacy, compliance, and security.

## Your Role
Backend Engineer

## Goal
Implement backend services that support the planned workflows, validation rules, and task sequencing.

## Technical Scope
API contracts, service logic, validation, error handling, integrations, and backend test coverage.

Relevant tasks:
- T1.1: Stakeholder Interviews & Requirements Gathering - Conduct interviews with patients, doctors, and administrative staff to understand current pain points, desired features, and workflow needs.
- T1.2: Technical Architecture Design - Design the high-level technical architecture, including technology stack, database schema, and API structure.
- T1.3: Compliance & Security Review - Identify and document all relevant healthcare regulations (e.g., HIPAA, GDPR) and define security protocols for data handling and platform access.
- T2.1: User Persona & Journey Mapping - Develop detailed user personas for patients, doctors, and admins, and map their typical journeys through the platform.
- T2.2: Wireframing & Low-Fidelity Prototyping - Create wireframes and low-fidelity prototypes for key screens and workflows.
- T2.3: UI/UX Design & High-Fidelity Prototyping - Develop the visual design (UI) and create high-fidelity interactive prototypes for patient, doctor, and admin portals.
- T2.4: Design Review & User Feedback - Conduct internal and external reviews of the prototypes to gather feedback and iterate on designs.
- T3.1: Database Development - Implement the database schema based on the technical design, including tables, relationships, and indexing.
- T3.2: Backend API Development - Develop the core backend APIs for user authentication, appointment management, patient records, notifications, etc.
- T3.3: Patient Portal Development - Build the frontend interface for patients to schedule, view, and manage appointments, and access their information.
- T3.4: Doctor Portal Development - Build the frontend interface for doctors to view schedules, manage appointments, and access patient details.
- T3.5: Admin Portal Development - Build the frontend interface for administrators to manage users, schedules, settings, and generate reports.
- T3.6: Integration Development (Optional) - Develop integrations with existing EHR/EMR systems or other third-party services (e.g., payment gateways, telehealth platforms).
- T4.1: Unit & Integration Testing - Perform unit tests on individual code components and integration tests on modules and API interactions.
- T4.2: System & End-to-End Testing - Conduct comprehensive system testing to verify all functionalities across the entire platform and end-to-end user flows.
- T4.3: Security & Performance Testing - Perform penetration testing, vulnerability assessments, and load/stress testing to ensure platform security and performance under expected loads.
- T4.4: User Acceptance Testing (UAT) - Engage key stakeholders (patients, doctors, admins) to test the platform in a simulated environment and provide final approval.
- T4.5: Bug Fixing & Regression Testing - Address all identified bugs and perform regression testing to ensure fixes haven't introduced new issues.
- T5.1: Infrastructure Setup & Configuration - Provision and configure production servers, databases, and network infrastructure.
- T5.2: Deployment to Production - Deploy the tested and approved application code to the production environment.
- T5.3: Data Migration (if applicable) - Migrate existing patient, doctor, or appointment data into the new platform.
- T5.4: User Training & Onboarding - Provide training sessions and documentation for doctors, admins, and potentially patients on how to use the new platform.
- T5.5: Go-Live & Monitoring Setup - Officially launch the platform and set up continuous monitoring for performance, errors, and security.
- T6.1: Continuous Monitoring & Incident Response - Monitor platform health, performance, and security, and respond to any incidents or outages.
- T6.2: Bug Fixes & Minor Enhancements - Address any post-launch bugs and implement small, immediate improvements based on user feedback.
- T6.3: Feedback Collection & Analysis - Establish channels for user feedback (e.g., surveys, support tickets) and regularly analyze it for insights.
- T6.4: Feature Backlog & Roadmap Planning - Based on feedback and strategic goals, maintain a backlog of new features and plan future development iterations.

Risks to account for:
- Failure to comply with healthcare data privacy regulations (e.g., HIPAA, GDPR).
- Difficulty integrating with existing Electronic Health Record (EHR) or Electronic Medical Record (EMR) systems.
- Low user adoption by patients, doctors, or administrative staff.
- Scope creep due to evolving requirements or new feature requests during development.
- Security breaches or data loss due to vulnerabilities in the platform.

Recommendations to preserve:
- Appoint a dedicated compliance and security lead for the project.
- Adopt an Agile development methodology with iterative releases.
- Establish a 'Champion User' program for early adopters among doctors and admins.
- Design the platform with cloud-native principles for scalability and resilience.

Assumptions to keep visible:
- Key stakeholders (patients, doctors, administrative staff) will be available for interviews, feedback, and User Acceptance Testing (UAT) as needed.
- Necessary infrastructure (cloud accounts, development environments) will be provisioned and accessible in a timely manner.
- A clear Minimum Viable Product (MVP) scope will be agreed upon before the development phase begins to manage expectations and control scope.
- Budget and resources (development team, QA, UX, DevOps) are sufficient for a 'medium' complexity project as outlined.
- Existing healthcare systems (if any) have documented APIs or clear data export capabilities for potential integration or migration.

## Related Phases
- P1: Discovery & Planning (4-6 weeks) - To gather detailed requirements, define the project scope, and establish the foundational technical and compliance architecture.
- P2: Design & Prototyping (5-7 weeks) - To create intuitive and user-friendly interfaces for all user roles and validate design concepts with stakeholders.
- P3: Development (12-16 weeks) - To build the backend infrastructure, APIs, and frontend user interfaces for all platform components.
- P4: Testing & Quality Assurance (6-8 weeks) - To ensure the platform is robust, secure, compliant, and meets all functional and non-functional requirements.
- P5: Deployment & Launch (2-3 weeks) - To successfully deploy the platform to the production environment and make it available to end-users.
- P6: Post-Launch Support & Iteration (Ongoing) - To provide ongoing support, address issues, gather feedback, and plan for future enhancements.

## Constraints
- Use the generated project plan as the source of truth.
- Do not build, deploy, or modify software from inside the planner.
- Keep implementation guidance appropriate for Codex, Cursor, Claude Code, Claude, GitHub Copilot, Lovable, or Bolt.
- Key stakeholders (patients, doctors, administrative staff) will be available for interviews, feedback, and User Acceptance Testing (UAT) as needed.
- Necessary infrastructure (cloud accounts, development environments) will be provisioned and accessible in a timely manner.
- A clear Minimum Viable Product (MVP) scope will be agreed upon before the development phase begins to manage expectations and control scope.
- Budget and resources (development team, QA, UX, DevOps) are sufficient for a 'medium' complexity project as outlined.
- Existing healthcare systems (if any) have documented APIs or clear data export capabilities for potential integration or migration.
- Healthcare workflows may require privacy, compliance, and security review.

## Expected Output
Produce implementation guidance or artifacts for Codex, Cursor, Claude Code, Claude, GitHub Copilot, Lovable, or Bolt. The output should be ready for an engineer to review and apply externally.
The planner itself must not build, deploy, or modify software.

## Acceptance Criteria
- The Backend Engineer output is aligned with the validated project plan.
- Relevant phases, tasks, assumptions, risks, and recommendations are addressed.
- The output is structured for engineer review before use in an external AI coding tool.
- Comprehensive list of functional and non-functional requirements documented.
- User stories and use cases defined for each user type.
- Technical Design Document (TDD) approved.

## Do Not Do
- Do not build or deploy the application automatically.
- Do not invent requirements, credentials, budgets, deadlines, integrations, or production infrastructure.
- Do not remove assumptions, warnings, risks, or acceptance criteria from the engineering handoff.
- Do not treat this prompt as a substitute for engineer review.
```

### Database Engineer implementation prompt

**Target Role:** Database Engineer  
**Target Tool:** Codex, Cursor, Claude Code, Claude, GitHub Copilot, Lovable, or Bolt  
**Purpose:** Define storage structures that support the project requirements without inventing unsupported data sources.

**Related Phases:**
- P1
- P2
- P3
- P4
- P5
- P6

**Constraints:**
- Use the generated project plan as the source of truth.
- Do not build, deploy, or modify software from inside the planner.
- Keep implementation guidance appropriate for Codex, Cursor, Claude Code, Claude, GitHub Copilot, Lovable, or Bolt.
- Key stakeholders (patients, doctors, administrative staff) will be available for interviews, feedback, and User Acceptance Testing (UAT) as needed.
- Necessary infrastructure (cloud accounts, development environments) will be provisioned and accessible in a timely manner.
- A clear Minimum Viable Product (MVP) scope will be agreed upon before the development phase begins to manage expectations and control scope.
- Budget and resources (development team, QA, UX, DevOps) are sufficient for a 'medium' complexity project as outlined.
- Existing healthcare systems (if any) have documented APIs or clear data export capabilities for potential integration or migration.
- Healthcare workflows may require privacy, compliance, and security review.

**Acceptance Criteria:**
- The Database Engineer output is aligned with the validated project plan.
- Relevant phases, tasks, assumptions, risks, and recommendations are addressed.
- The output is structured for engineer review before use in an external AI coding tool.
- Comprehensive list of functional and non-functional requirements documented.
- User stories and use cases defined for each user type.
- Technical Design Document (TDD) approved.

**Prompt:**
```text
You are a senior database engineer responsible for designing the data model and persistence approach.

## Project Context
Project name: Healthcare Appointment Platform
Project description: Build a healthcare appointment platform for patients, doctors, and admins
Domain: healthcare
Project type: healthcare workflow improvement
Complexity: medium
Summary: This project aims to develop a comprehensive healthcare appointment platform designed to serve patients, doctors, and administrative staff. The platform will streamline the appointment scheduling process, improve communication, and enhance overall workflow efficiency within a healthcare setting. Given the healthcare domain, significant attention will be paid to privacy, compliance, and security.

## Your Role
Database Engineer

## Goal
Define storage structures that support the project requirements without inventing unsupported data sources.

## Technical Scope
Entities, relationships, indexes, migrations, data quality checks, retention needs, and backup assumptions.

Relevant tasks:
- T1.1: Stakeholder Interviews & Requirements Gathering - Conduct interviews with patients, doctors, and administrative staff to understand current pain points, desired features, and workflow needs.
- T1.2: Technical Architecture Design - Design the high-level technical architecture, including technology stack, database schema, and API structure.
- T1.3: Compliance & Security Review - Identify and document all relevant healthcare regulations (e.g., HIPAA, GDPR) and define security protocols for data handling and platform access.
- T2.1: User Persona & Journey Mapping - Develop detailed user personas for patients, doctors, and admins, and map their typical journeys through the platform.
- T2.2: Wireframing & Low-Fidelity Prototyping - Create wireframes and low-fidelity prototypes for key screens and workflows.
- T2.3: UI/UX Design & High-Fidelity Prototyping - Develop the visual design (UI) and create high-fidelity interactive prototypes for patient, doctor, and admin portals.
- T2.4: Design Review & User Feedback - Conduct internal and external reviews of the prototypes to gather feedback and iterate on designs.
- T3.1: Database Development - Implement the database schema based on the technical design, including tables, relationships, and indexing.
- T3.2: Backend API Development - Develop the core backend APIs for user authentication, appointment management, patient records, notifications, etc.
- T3.3: Patient Portal Development - Build the frontend interface for patients to schedule, view, and manage appointments, and access their information.
- T3.4: Doctor Portal Development - Build the frontend interface for doctors to view schedules, manage appointments, and access patient details.
- T3.5: Admin Portal Development - Build the frontend interface for administrators to manage users, schedules, settings, and generate reports.
- T3.6: Integration Development (Optional) - Develop integrations with existing EHR/EMR systems or other third-party services (e.g., payment gateways, telehealth platforms).
- T4.1: Unit & Integration Testing - Perform unit tests on individual code components and integration tests on modules and API interactions.
- T4.2: System & End-to-End Testing - Conduct comprehensive system testing to verify all functionalities across the entire platform and end-to-end user flows.
- T4.3: Security & Performance Testing - Perform penetration testing, vulnerability assessments, and load/stress testing to ensure platform security and performance under expected loads.
- T4.4: User Acceptance Testing (UAT) - Engage key stakeholders (patients, doctors, admins) to test the platform in a simulated environment and provide final approval.
- T4.5: Bug Fixing & Regression Testing - Address all identified bugs and perform regression testing to ensure fixes haven't introduced new issues.
- T5.1: Infrastructure Setup & Configuration - Provision and configure production servers, databases, and network infrastructure.
- T5.2: Deployment to Production - Deploy the tested and approved application code to the production environment.
- T5.3: Data Migration (if applicable) - Migrate existing patient, doctor, or appointment data into the new platform.
- T5.4: User Training & Onboarding - Provide training sessions and documentation for doctors, admins, and potentially patients on how to use the new platform.
- T5.5: Go-Live & Monitoring Setup - Officially launch the platform and set up continuous monitoring for performance, errors, and security.
- T6.1: Continuous Monitoring & Incident Response - Monitor platform health, performance, and security, and respond to any incidents or outages.
- T6.2: Bug Fixes & Minor Enhancements - Address any post-launch bugs and implement small, immediate improvements based on user feedback.
- T6.3: Feedback Collection & Analysis - Establish channels for user feedback (e.g., surveys, support tickets) and regularly analyze it for insights.
- T6.4: Feature Backlog & Roadmap Planning - Based on feedback and strategic goals, maintain a backlog of new features and plan future development iterations.

Risks to account for:
- Failure to comply with healthcare data privacy regulations (e.g., HIPAA, GDPR).
- Difficulty integrating with existing Electronic Health Record (EHR) or Electronic Medical Record (EMR) systems.
- Low user adoption by patients, doctors, or administrative staff.
- Scope creep due to evolving requirements or new feature requests during development.
- Security breaches or data loss due to vulnerabilities in the platform.

Recommendations to preserve:
- Appoint a dedicated compliance and security lead for the project.
- Adopt an Agile development methodology with iterative releases.
- Establish a 'Champion User' program for early adopters among doctors and admins.
- Design the platform with cloud-native principles for scalability and resilience.

Assumptions to keep visible:
- Key stakeholders (patients, doctors, administrative staff) will be available for interviews, feedback, and User Acceptance Testing (UAT) as needed.
- Necessary infrastructure (cloud accounts, development environments) will be provisioned and accessible in a timely manner.
- A clear Minimum Viable Product (MVP) scope will be agreed upon before the development phase begins to manage expectations and control scope.
- Budget and resources (development team, QA, UX, DevOps) are sufficient for a 'medium' complexity project as outlined.
- Existing healthcare systems (if any) have documented APIs or clear data export capabilities for potential integration or migration.

## Related Phases
- P1: Discovery & Planning (4-6 weeks) - To gather detailed requirements, define the project scope, and establish the foundational technical and compliance architecture.
- P2: Design & Prototyping (5-7 weeks) - To create intuitive and user-friendly interfaces for all user roles and validate design concepts with stakeholders.
- P3: Development (12-16 weeks) - To build the backend infrastructure, APIs, and frontend user interfaces for all platform components.
- P4: Testing & Quality Assurance (6-8 weeks) - To ensure the platform is robust, secure, compliant, and meets all functional and non-functional requirements.
- P5: Deployment & Launch (2-3 weeks) - To successfully deploy the platform to the production environment and make it available to end-users.
- P6: Post-Launch Support & Iteration (Ongoing) - To provide ongoing support, address issues, gather feedback, and plan for future enhancements.

## Constraints
- Use the generated project plan as the source of truth.
- Do not build, deploy, or modify software from inside the planner.
- Keep implementation guidance appropriate for Codex, Cursor, Claude Code, Claude, GitHub Copilot, Lovable, or Bolt.
- Key stakeholders (patients, doctors, administrative staff) will be available for interviews, feedback, and User Acceptance Testing (UAT) as needed.
- Necessary infrastructure (cloud accounts, development environments) will be provisioned and accessible in a timely manner.
- A clear Minimum Viable Product (MVP) scope will be agreed upon before the development phase begins to manage expectations and control scope.
- Budget and resources (development team, QA, UX, DevOps) are sufficient for a 'medium' complexity project as outlined.
- Existing healthcare systems (if any) have documented APIs or clear data export capabilities for potential integration or migration.
- Healthcare workflows may require privacy, compliance, and security review.

## Expected Output
Produce implementation guidance or artifacts for Codex, Cursor, Claude Code, Claude, GitHub Copilot, Lovable, or Bolt. The output should be ready for an engineer to review and apply externally.
The planner itself must not build, deploy, or modify software.

## Acceptance Criteria
- The Database Engineer output is aligned with the validated project plan.
- Relevant phases, tasks, assumptions, risks, and recommendations are addressed.
- The output is structured for engineer review before use in an external AI coding tool.
- Comprehensive list of functional and non-functional requirements documented.
- User stories and use cases defined for each user type.
- Technical Design Document (TDD) approved.

## Do Not Do
- Do not build or deploy the application automatically.
- Do not invent requirements, credentials, budgets, deadlines, integrations, or production infrastructure.
- Do not remove assumptions, warnings, risks, or acceptance criteria from the engineering handoff.
- Do not treat this prompt as a substitute for engineer review.
```

### QA / Testing Engineer implementation prompt

**Target Role:** QA / Testing Engineer  
**Target Tool:** Codex, Cursor, Claude Code, Claude, GitHub Copilot, Lovable, or Bolt  
**Purpose:** Create a practical test strategy for the project phases, risks, acceptance criteria, and release workflow.

**Related Phases:**
- P1
- P2
- P3
- P4
- P5
- P6

**Constraints:**
- Use the generated project plan as the source of truth.
- Do not build, deploy, or modify software from inside the planner.
- Keep implementation guidance appropriate for Codex, Cursor, Claude Code, Claude, GitHub Copilot, Lovable, or Bolt.
- Key stakeholders (patients, doctors, administrative staff) will be available for interviews, feedback, and User Acceptance Testing (UAT) as needed.
- Necessary infrastructure (cloud accounts, development environments) will be provisioned and accessible in a timely manner.
- A clear Minimum Viable Product (MVP) scope will be agreed upon before the development phase begins to manage expectations and control scope.
- Budget and resources (development team, QA, UX, DevOps) are sufficient for a 'medium' complexity project as outlined.
- Existing healthcare systems (if any) have documented APIs or clear data export capabilities for potential integration or migration.
- Healthcare workflows may require privacy, compliance, and security review.

**Acceptance Criteria:**
- The QA / Testing Engineer output is aligned with the validated project plan.
- Relevant phases, tasks, assumptions, risks, and recommendations are addressed.
- The output is structured for engineer review before use in an external AI coding tool.
- Comprehensive list of functional and non-functional requirements documented.
- User stories and use cases defined for each user type.
- Technical Design Document (TDD) approved.

**Prompt:**
```text
You are a senior QA engineer responsible for validating the implementation against the plan.

## Project Context
Project name: Healthcare Appointment Platform
Project description: Build a healthcare appointment platform for patients, doctors, and admins
Domain: healthcare
Project type: healthcare workflow improvement
Complexity: medium
Summary: This project aims to develop a comprehensive healthcare appointment platform designed to serve patients, doctors, and administrative staff. The platform will streamline the appointment scheduling process, improve communication, and enhance overall workflow efficiency within a healthcare setting. Given the healthcare domain, significant attention will be paid to privacy, compliance, and security.

## Your Role
QA / Testing Engineer

## Goal
Create a practical test strategy for the project phases, risks, acceptance criteria, and release workflow.

## Technical Scope
Functional tests, regression tests, edge cases, acceptance criteria validation, risk-based testing, and defect reporting.

Relevant tasks:
- T1.1: Stakeholder Interviews & Requirements Gathering - Conduct interviews with patients, doctors, and administrative staff to understand current pain points, desired features, and workflow needs.
- T1.2: Technical Architecture Design - Design the high-level technical architecture, including technology stack, database schema, and API structure.
- T1.3: Compliance & Security Review - Identify and document all relevant healthcare regulations (e.g., HIPAA, GDPR) and define security protocols for data handling and platform access.
- T2.1: User Persona & Journey Mapping - Develop detailed user personas for patients, doctors, and admins, and map their typical journeys through the platform.
- T2.2: Wireframing & Low-Fidelity Prototyping - Create wireframes and low-fidelity prototypes for key screens and workflows.
- T2.3: UI/UX Design & High-Fidelity Prototyping - Develop the visual design (UI) and create high-fidelity interactive prototypes for patient, doctor, and admin portals.
- T2.4: Design Review & User Feedback - Conduct internal and external reviews of the prototypes to gather feedback and iterate on designs.
- T3.1: Database Development - Implement the database schema based on the technical design, including tables, relationships, and indexing.
- T3.2: Backend API Development - Develop the core backend APIs for user authentication, appointment management, patient records, notifications, etc.
- T3.3: Patient Portal Development - Build the frontend interface for patients to schedule, view, and manage appointments, and access their information.
- T3.4: Doctor Portal Development - Build the frontend interface for doctors to view schedules, manage appointments, and access patient details.
- T3.5: Admin Portal Development - Build the frontend interface for administrators to manage users, schedules, settings, and generate reports.
- T3.6: Integration Development (Optional) - Develop integrations with existing EHR/EMR systems or other third-party services (e.g., payment gateways, telehealth platforms).
- T4.1: Unit & Integration Testing - Perform unit tests on individual code components and integration tests on modules and API interactions.
- T4.2: System & End-to-End Testing - Conduct comprehensive system testing to verify all functionalities across the entire platform and end-to-end user flows.
- T4.3: Security & Performance Testing - Perform penetration testing, vulnerability assessments, and load/stress testing to ensure platform security and performance under expected loads.
- T4.4: User Acceptance Testing (UAT) - Engage key stakeholders (patients, doctors, admins) to test the platform in a simulated environment and provide final approval.
- T4.5: Bug Fixing & Regression Testing - Address all identified bugs and perform regression testing to ensure fixes haven't introduced new issues.
- T5.1: Infrastructure Setup & Configuration - Provision and configure production servers, databases, and network infrastructure.
- T5.2: Deployment to Production - Deploy the tested and approved application code to the production environment.
- T5.3: Data Migration (if applicable) - Migrate existing patient, doctor, or appointment data into the new platform.
- T5.4: User Training & Onboarding - Provide training sessions and documentation for doctors, admins, and potentially patients on how to use the new platform.
- T5.5: Go-Live & Monitoring Setup - Officially launch the platform and set up continuous monitoring for performance, errors, and security.
- T6.1: Continuous Monitoring & Incident Response - Monitor platform health, performance, and security, and respond to any incidents or outages.
- T6.2: Bug Fixes & Minor Enhancements - Address any post-launch bugs and implement small, immediate improvements based on user feedback.
- T6.3: Feedback Collection & Analysis - Establish channels for user feedback (e.g., surveys, support tickets) and regularly analyze it for insights.
- T6.4: Feature Backlog & Roadmap Planning - Based on feedback and strategic goals, maintain a backlog of new features and plan future development iterations.

Risks to account for:
- Failure to comply with healthcare data privacy regulations (e.g., HIPAA, GDPR).
- Difficulty integrating with existing Electronic Health Record (EHR) or Electronic Medical Record (EMR) systems.
- Low user adoption by patients, doctors, or administrative staff.
- Scope creep due to evolving requirements or new feature requests during development.
- Security breaches or data loss due to vulnerabilities in the platform.

Recommendations to preserve:
- Appoint a dedicated compliance and security lead for the project.
- Adopt an Agile development methodology with iterative releases.
- Establish a 'Champion User' program for early adopters among doctors and admins.
- Design the platform with cloud-native principles for scalability and resilience.

Assumptions to keep visible:
- Key stakeholders (patients, doctors, administrative staff) will be available for interviews, feedback, and User Acceptance Testing (UAT) as needed.
- Necessary infrastructure (cloud accounts, development environments) will be provisioned and accessible in a timely manner.
- A clear Minimum Viable Product (MVP) scope will be agreed upon before the development phase begins to manage expectations and control scope.
- Budget and resources (development team, QA, UX, DevOps) are sufficient for a 'medium' complexity project as outlined.
- Existing healthcare systems (if any) have documented APIs or clear data export capabilities for potential integration or migration.

## Related Phases
- P1: Discovery & Planning (4-6 weeks) - To gather detailed requirements, define the project scope, and establish the foundational technical and compliance architecture.
- P2: Design & Prototyping (5-7 weeks) - To create intuitive and user-friendly interfaces for all user roles and validate design concepts with stakeholders.
- P3: Development (12-16 weeks) - To build the backend infrastructure, APIs, and frontend user interfaces for all platform components.
- P4: Testing & Quality Assurance (6-8 weeks) - To ensure the platform is robust, secure, compliant, and meets all functional and non-functional requirements.
- P5: Deployment & Launch (2-3 weeks) - To successfully deploy the platform to the production environment and make it available to end-users.
- P6: Post-Launch Support & Iteration (Ongoing) - To provide ongoing support, address issues, gather feedback, and plan for future enhancements.

## Constraints
- Use the generated project plan as the source of truth.
- Do not build, deploy, or modify software from inside the planner.
- Keep implementation guidance appropriate for Codex, Cursor, Claude Code, Claude, GitHub Copilot, Lovable, or Bolt.
- Key stakeholders (patients, doctors, administrative staff) will be available for interviews, feedback, and User Acceptance Testing (UAT) as needed.
- Necessary infrastructure (cloud accounts, development environments) will be provisioned and accessible in a timely manner.
- A clear Minimum Viable Product (MVP) scope will be agreed upon before the development phase begins to manage expectations and control scope.
- Budget and resources (development team, QA, UX, DevOps) are sufficient for a 'medium' complexity project as outlined.
- Existing healthcare systems (if any) have documented APIs or clear data export capabilities for potential integration or migration.
- Healthcare workflows may require privacy, compliance, and security review.

## Expected Output
Produce implementation guidance or artifacts for Codex, Cursor, Claude Code, Claude, GitHub Copilot, Lovable, or Bolt. The output should be ready for an engineer to review and apply externally.
The planner itself must not build, deploy, or modify software.

## Acceptance Criteria
- The QA / Testing Engineer output is aligned with the validated project plan.
- Relevant phases, tasks, assumptions, risks, and recommendations are addressed.
- The output is structured for engineer review before use in an external AI coding tool.
- Comprehensive list of functional and non-functional requirements documented.
- User stories and use cases defined for each user type.
- Technical Design Document (TDD) approved.

## Do Not Do
- Do not build or deploy the application automatically.
- Do not invent requirements, credentials, budgets, deadlines, integrations, or production infrastructure.
- Do not remove assumptions, warnings, risks, or acceptance criteria from the engineering handoff.
- Do not treat this prompt as a substitute for engineer review.
```

### DevOps Engineer implementation prompt

**Target Role:** DevOps Engineer  
**Target Tool:** Codex, Cursor, Claude Code, Claude, GitHub Copilot, Lovable, or Bolt  
**Purpose:** Plan environment, build, release, monitoring, and rollback work without deploying anything automatically.

**Related Phases:**
- P1
- P2
- P3
- P4
- P5
- P6

**Constraints:**
- Use the generated project plan as the source of truth.
- Do not build, deploy, or modify software from inside the planner.
- Keep implementation guidance appropriate for Codex, Cursor, Claude Code, Claude, GitHub Copilot, Lovable, or Bolt.
- Key stakeholders (patients, doctors, administrative staff) will be available for interviews, feedback, and User Acceptance Testing (UAT) as needed.
- Necessary infrastructure (cloud accounts, development environments) will be provisioned and accessible in a timely manner.
- A clear Minimum Viable Product (MVP) scope will be agreed upon before the development phase begins to manage expectations and control scope.
- Budget and resources (development team, QA, UX, DevOps) are sufficient for a 'medium' complexity project as outlined.
- Existing healthcare systems (if any) have documented APIs or clear data export capabilities for potential integration or migration.
- Healthcare workflows may require privacy, compliance, and security review.

**Acceptance Criteria:**
- The DevOps Engineer output is aligned with the validated project plan.
- Relevant phases, tasks, assumptions, risks, and recommendations are addressed.
- The output is structured for engineer review before use in an external AI coding tool.
- Comprehensive list of functional and non-functional requirements documented.
- User stories and use cases defined for each user type.
- Technical Design Document (TDD) approved.

**Prompt:**
```text
You are a senior DevOps engineer responsible for deployment readiness and operational workflow.

## Project Context
Project name: Healthcare Appointment Platform
Project description: Build a healthcare appointment platform for patients, doctors, and admins
Domain: healthcare
Project type: healthcare workflow improvement
Complexity: medium
Summary: This project aims to develop a comprehensive healthcare appointment platform designed to serve patients, doctors, and administrative staff. The platform will streamline the appointment scheduling process, improve communication, and enhance overall workflow efficiency within a healthcare setting. Given the healthcare domain, significant attention will be paid to privacy, compliance, and security.

## Your Role
DevOps Engineer

## Goal
Plan environment, build, release, monitoring, and rollback work without deploying anything automatically.

## Technical Scope
Local development setup, CI checks, configuration, deployment plan, observability, release checklist, and rollback notes.

Relevant tasks:
- T1.1: Stakeholder Interviews & Requirements Gathering - Conduct interviews with patients, doctors, and administrative staff to understand current pain points, desired features, and workflow needs.
- T1.2: Technical Architecture Design - Design the high-level technical architecture, including technology stack, database schema, and API structure.
- T1.3: Compliance & Security Review - Identify and document all relevant healthcare regulations (e.g., HIPAA, GDPR) and define security protocols for data handling and platform access.
- T2.1: User Persona & Journey Mapping - Develop detailed user personas for patients, doctors, and admins, and map their typical journeys through the platform.
- T2.2: Wireframing & Low-Fidelity Prototyping - Create wireframes and low-fidelity prototypes for key screens and workflows.
- T2.3: UI/UX Design & High-Fidelity Prototyping - Develop the visual design (UI) and create high-fidelity interactive prototypes for patient, doctor, and admin portals.
- T2.4: Design Review & User Feedback - Conduct internal and external reviews of the prototypes to gather feedback and iterate on designs.
- T3.1: Database Development - Implement the database schema based on the technical design, including tables, relationships, and indexing.
- T3.2: Backend API Development - Develop the core backend APIs for user authentication, appointment management, patient records, notifications, etc.
- T3.3: Patient Portal Development - Build the frontend interface for patients to schedule, view, and manage appointments, and access their information.
- T3.4: Doctor Portal Development - Build the frontend interface for doctors to view schedules, manage appointments, and access patient details.
- T3.5: Admin Portal Development - Build the frontend interface for administrators to manage users, schedules, settings, and generate reports.
- T3.6: Integration Development (Optional) - Develop integrations with existing EHR/EMR systems or other third-party services (e.g., payment gateways, telehealth platforms).
- T4.1: Unit & Integration Testing - Perform unit tests on individual code components and integration tests on modules and API interactions.
- T4.2: System & End-to-End Testing - Conduct comprehensive system testing to verify all functionalities across the entire platform and end-to-end user flows.
- T4.3: Security & Performance Testing - Perform penetration testing, vulnerability assessments, and load/stress testing to ensure platform security and performance under expected loads.
- T4.4: User Acceptance Testing (UAT) - Engage key stakeholders (patients, doctors, admins) to test the platform in a simulated environment and provide final approval.
- T4.5: Bug Fixing & Regression Testing - Address all identified bugs and perform regression testing to ensure fixes haven't introduced new issues.
- T5.1: Infrastructure Setup & Configuration - Provision and configure production servers, databases, and network infrastructure.
- T5.2: Deployment to Production - Deploy the tested and approved application code to the production environment.
- T5.3: Data Migration (if applicable) - Migrate existing patient, doctor, or appointment data into the new platform.
- T5.4: User Training & Onboarding - Provide training sessions and documentation for doctors, admins, and potentially patients on how to use the new platform.
- T5.5: Go-Live & Monitoring Setup - Officially launch the platform and set up continuous monitoring for performance, errors, and security.
- T6.1: Continuous Monitoring & Incident Response - Monitor platform health, performance, and security, and respond to any incidents or outages.
- T6.2: Bug Fixes & Minor Enhancements - Address any post-launch bugs and implement small, immediate improvements based on user feedback.
- T6.3: Feedback Collection & Analysis - Establish channels for user feedback (e.g., surveys, support tickets) and regularly analyze it for insights.
- T6.4: Feature Backlog & Roadmap Planning - Based on feedback and strategic goals, maintain a backlog of new features and plan future development iterations.

Risks to account for:
- Failure to comply with healthcare data privacy regulations (e.g., HIPAA, GDPR).
- Difficulty integrating with existing Electronic Health Record (EHR) or Electronic Medical Record (EMR) systems.
- Low user adoption by patients, doctors, or administrative staff.
- Scope creep due to evolving requirements or new feature requests during development.
- Security breaches or data loss due to vulnerabilities in the platform.

Recommendations to preserve:
- Appoint a dedicated compliance and security lead for the project.
- Adopt an Agile development methodology with iterative releases.
- Establish a 'Champion User' program for early adopters among doctors and admins.
- Design the platform with cloud-native principles for scalability and resilience.

Assumptions to keep visible:
- Key stakeholders (patients, doctors, administrative staff) will be available for interviews, feedback, and User Acceptance Testing (UAT) as needed.
- Necessary infrastructure (cloud accounts, development environments) will be provisioned and accessible in a timely manner.
- A clear Minimum Viable Product (MVP) scope will be agreed upon before the development phase begins to manage expectations and control scope.
- Budget and resources (development team, QA, UX, DevOps) are sufficient for a 'medium' complexity project as outlined.
- Existing healthcare systems (if any) have documented APIs or clear data export capabilities for potential integration or migration.

## Related Phases
- P1: Discovery & Planning (4-6 weeks) - To gather detailed requirements, define the project scope, and establish the foundational technical and compliance architecture.
- P2: Design & Prototyping (5-7 weeks) - To create intuitive and user-friendly interfaces for all user roles and validate design concepts with stakeholders.
- P3: Development (12-16 weeks) - To build the backend infrastructure, APIs, and frontend user interfaces for all platform components.
- P4: Testing & Quality Assurance (6-8 weeks) - To ensure the platform is robust, secure, compliant, and meets all functional and non-functional requirements.
- P5: Deployment & Launch (2-3 weeks) - To successfully deploy the platform to the production environment and make it available to end-users.
- P6: Post-Launch Support & Iteration (Ongoing) - To provide ongoing support, address issues, gather feedback, and plan for future enhancements.

## Constraints
- Use the generated project plan as the source of truth.
- Do not build, deploy, or modify software from inside the planner.
- Keep implementation guidance appropriate for Codex, Cursor, Claude Code, Claude, GitHub Copilot, Lovable, or Bolt.
- Key stakeholders (patients, doctors, administrative staff) will be available for interviews, feedback, and User Acceptance Testing (UAT) as needed.
- Necessary infrastructure (cloud accounts, development environments) will be provisioned and accessible in a timely manner.
- A clear Minimum Viable Product (MVP) scope will be agreed upon before the development phase begins to manage expectations and control scope.
- Budget and resources (development team, QA, UX, DevOps) are sufficient for a 'medium' complexity project as outlined.
- Existing healthcare systems (if any) have documented APIs or clear data export capabilities for potential integration or migration.
- Healthcare workflows may require privacy, compliance, and security review.

## Expected Output
Produce implementation guidance or artifacts for Codex, Cursor, Claude Code, Claude, GitHub Copilot, Lovable, or Bolt. The output should be ready for an engineer to review and apply externally.
The planner itself must not build, deploy, or modify software.

## Acceptance Criteria
- The DevOps Engineer output is aligned with the validated project plan.
- Relevant phases, tasks, assumptions, risks, and recommendations are addressed.
- The output is structured for engineer review before use in an external AI coding tool.
- Comprehensive list of functional and non-functional requirements documented.
- User stories and use cases defined for each user type.
- Technical Design Document (TDD) approved.

## Do Not Do
- Do not build or deploy the application automatically.
- Do not invent requirements, credentials, budgets, deadlines, integrations, or production infrastructure.
- Do not remove assumptions, warnings, risks, or acceptance criteria from the engineering handoff.
- Do not treat this prompt as a substitute for engineer review.
```

### Security Reviewer implementation prompt

**Target Role:** Security Reviewer  
**Target Tool:** Codex, Cursor, Claude Code, Claude, GitHub Copilot, Lovable, or Bolt  
**Purpose:** Review implementation plans for security, privacy, access control, data handling, and compliance risks.

**Related Phases:**
- P1
- P2
- P3
- P4
- P5
- P6

**Constraints:**
- Use the generated project plan as the source of truth.
- Do not build, deploy, or modify software from inside the planner.
- Keep implementation guidance appropriate for Codex, Cursor, Claude Code, Claude, GitHub Copilot, Lovable, or Bolt.
- Key stakeholders (patients, doctors, administrative staff) will be available for interviews, feedback, and User Acceptance Testing (UAT) as needed.
- Necessary infrastructure (cloud accounts, development environments) will be provisioned and accessible in a timely manner.
- A clear Minimum Viable Product (MVP) scope will be agreed upon before the development phase begins to manage expectations and control scope.
- Budget and resources (development team, QA, UX, DevOps) are sufficient for a 'medium' complexity project as outlined.
- Existing healthcare systems (if any) have documented APIs or clear data export capabilities for potential integration or migration.
- Healthcare workflows may require privacy, compliance, and security review.

**Acceptance Criteria:**
- The Security Reviewer output is aligned with the validated project plan.
- Relevant phases, tasks, assumptions, risks, and recommendations are addressed.
- The output is structured for engineer review before use in an external AI coding tool.
- Comprehensive list of functional and non-functional requirements documented.
- User stories and use cases defined for each user type.
- Technical Design Document (TDD) approved.

**Prompt:**
```text
You are a senior security engineer responsible for reviewing the plan for security and privacy risks.

## Project Context
Project name: Healthcare Appointment Platform
Project description: Build a healthcare appointment platform for patients, doctors, and admins
Domain: healthcare
Project type: healthcare workflow improvement
Complexity: medium
Summary: This project aims to develop a comprehensive healthcare appointment platform designed to serve patients, doctors, and administrative staff. The platform will streamline the appointment scheduling process, improve communication, and enhance overall workflow efficiency within a healthcare setting. Given the healthcare domain, significant attention will be paid to privacy, compliance, and security.

## Your Role
Security Reviewer

## Goal
Review implementation plans for security, privacy, access control, data handling, and compliance risks.

## Technical Scope
Threat modeling, authentication and authorization concerns, sensitive data handling, dependency risk, and secure defaults.

Relevant tasks:
- T1.1: Stakeholder Interviews & Requirements Gathering - Conduct interviews with patients, doctors, and administrative staff to understand current pain points, desired features, and workflow needs.
- T1.2: Technical Architecture Design - Design the high-level technical architecture, including technology stack, database schema, and API structure.
- T1.3: Compliance & Security Review - Identify and document all relevant healthcare regulations (e.g., HIPAA, GDPR) and define security protocols for data handling and platform access.
- T2.1: User Persona & Journey Mapping - Develop detailed user personas for patients, doctors, and admins, and map their typical journeys through the platform.
- T2.2: Wireframing & Low-Fidelity Prototyping - Create wireframes and low-fidelity prototypes for key screens and workflows.
- T2.3: UI/UX Design & High-Fidelity Prototyping - Develop the visual design (UI) and create high-fidelity interactive prototypes for patient, doctor, and admin portals.
- T2.4: Design Review & User Feedback - Conduct internal and external reviews of the prototypes to gather feedback and iterate on designs.
- T3.1: Database Development - Implement the database schema based on the technical design, including tables, relationships, and indexing.
- T3.2: Backend API Development - Develop the core backend APIs for user authentication, appointment management, patient records, notifications, etc.
- T3.3: Patient Portal Development - Build the frontend interface for patients to schedule, view, and manage appointments, and access their information.
- T3.4: Doctor Portal Development - Build the frontend interface for doctors to view schedules, manage appointments, and access patient details.
- T3.5: Admin Portal Development - Build the frontend interface for administrators to manage users, schedules, settings, and generate reports.
- T3.6: Integration Development (Optional) - Develop integrations with existing EHR/EMR systems or other third-party services (e.g., payment gateways, telehealth platforms).
- T4.1: Unit & Integration Testing - Perform unit tests on individual code components and integration tests on modules and API interactions.
- T4.2: System & End-to-End Testing - Conduct comprehensive system testing to verify all functionalities across the entire platform and end-to-end user flows.
- T4.3: Security & Performance Testing - Perform penetration testing, vulnerability assessments, and load/stress testing to ensure platform security and performance under expected loads.
- T4.4: User Acceptance Testing (UAT) - Engage key stakeholders (patients, doctors, admins) to test the platform in a simulated environment and provide final approval.
- T4.5: Bug Fixing & Regression Testing - Address all identified bugs and perform regression testing to ensure fixes haven't introduced new issues.
- T5.1: Infrastructure Setup & Configuration - Provision and configure production servers, databases, and network infrastructure.
- T5.2: Deployment to Production - Deploy the tested and approved application code to the production environment.
- T5.3: Data Migration (if applicable) - Migrate existing patient, doctor, or appointment data into the new platform.
- T5.4: User Training & Onboarding - Provide training sessions and documentation for doctors, admins, and potentially patients on how to use the new platform.
- T5.5: Go-Live & Monitoring Setup - Officially launch the platform and set up continuous monitoring for performance, errors, and security.
- T6.1: Continuous Monitoring & Incident Response - Monitor platform health, performance, and security, and respond to any incidents or outages.
- T6.2: Bug Fixes & Minor Enhancements - Address any post-launch bugs and implement small, immediate improvements based on user feedback.
- T6.3: Feedback Collection & Analysis - Establish channels for user feedback (e.g., surveys, support tickets) and regularly analyze it for insights.
- T6.4: Feature Backlog & Roadmap Planning - Based on feedback and strategic goals, maintain a backlog of new features and plan future development iterations.

Risks to account for:
- Failure to comply with healthcare data privacy regulations (e.g., HIPAA, GDPR).
- Difficulty integrating with existing Electronic Health Record (EHR) or Electronic Medical Record (EMR) systems.
- Low user adoption by patients, doctors, or administrative staff.
- Scope creep due to evolving requirements or new feature requests during development.
- Security breaches or data loss due to vulnerabilities in the platform.

Recommendations to preserve:
- Appoint a dedicated compliance and security lead for the project.
- Adopt an Agile development methodology with iterative releases.
- Establish a 'Champion User' program for early adopters among doctors and admins.
- Design the platform with cloud-native principles for scalability and resilience.

Assumptions to keep visible:
- Key stakeholders (patients, doctors, administrative staff) will be available for interviews, feedback, and User Acceptance Testing (UAT) as needed.
- Necessary infrastructure (cloud accounts, development environments) will be provisioned and accessible in a timely manner.
- A clear Minimum Viable Product (MVP) scope will be agreed upon before the development phase begins to manage expectations and control scope.
- Budget and resources (development team, QA, UX, DevOps) are sufficient for a 'medium' complexity project as outlined.
- Existing healthcare systems (if any) have documented APIs or clear data export capabilities for potential integration or migration.

## Related Phases
- P1: Discovery & Planning (4-6 weeks) - To gather detailed requirements, define the project scope, and establish the foundational technical and compliance architecture.
- P2: Design & Prototyping (5-7 weeks) - To create intuitive and user-friendly interfaces for all user roles and validate design concepts with stakeholders.
- P3: Development (12-16 weeks) - To build the backend infrastructure, APIs, and frontend user interfaces for all platform components.
- P4: Testing & Quality Assurance (6-8 weeks) - To ensure the platform is robust, secure, compliant, and meets all functional and non-functional requirements.
- P5: Deployment & Launch (2-3 weeks) - To successfully deploy the platform to the production environment and make it available to end-users.
- P6: Post-Launch Support & Iteration (Ongoing) - To provide ongoing support, address issues, gather feedback, and plan for future enhancements.

## Constraints
- Use the generated project plan as the source of truth.
- Do not build, deploy, or modify software from inside the planner.
- Keep implementation guidance appropriate for Codex, Cursor, Claude Code, Claude, GitHub Copilot, Lovable, or Bolt.
- Key stakeholders (patients, doctors, administrative staff) will be available for interviews, feedback, and User Acceptance Testing (UAT) as needed.
- Necessary infrastructure (cloud accounts, development environments) will be provisioned and accessible in a timely manner.
- A clear Minimum Viable Product (MVP) scope will be agreed upon before the development phase begins to manage expectations and control scope.
- Budget and resources (development team, QA, UX, DevOps) are sufficient for a 'medium' complexity project as outlined.
- Existing healthcare systems (if any) have documented APIs or clear data export capabilities for potential integration or migration.
- Healthcare workflows may require privacy, compliance, and security review.

## Expected Output
Produce implementation guidance or artifacts for Codex, Cursor, Claude Code, Claude, GitHub Copilot, Lovable, or Bolt. The output should be ready for an engineer to review and apply externally.
The planner itself must not build, deploy, or modify software.

## Acceptance Criteria
- The Security Reviewer output is aligned with the validated project plan.
- Relevant phases, tasks, assumptions, risks, and recommendations are addressed.
- The output is structured for engineer review before use in an external AI coding tool.
- Comprehensive list of functional and non-functional requirements documented.
- User stories and use cases defined for each user type.
- Technical Design Document (TDD) approved.

## Do Not Do
- Do not build or deploy the application automatically.
- Do not invent requirements, credentials, budgets, deadlines, integrations, or production infrastructure.
- Do not remove assumptions, warnings, risks, or acceptance criteria from the engineering handoff.
- Do not treat this prompt as a substitute for engineer review.
```

## Prompt Quality Evaluations
### Evaluation for EP1

- Score: 100/100
- Ready to use: True

**Strengths:**
- Prompt starts with senior role framing.
- Prompt includes all required structure sections.
- Prompt has enough detail for engineering use.
- Prompt names the target role.
- Prompt identifies target AI coding tools.
- Prompt is tied to related plan phases.
- Prompt purpose is reflected in the prompt text.
- Prompt includes project-specific metadata.
- Prompt includes technical scope.
- Prompt includes meaningful constraints.
- Prompt references risk handling.
- Prompt references implementation tasks.
- Prompt preserves the product boundary.
- Prompt includes an Expected Output section.
- Prompt is positioned for external AI coding tools.
- Prompt keeps engineer review in the workflow.
- Prompt describes the expected deliverable type.
- Prompt includes an Acceptance Criteria section.
- Prompt includes meaningful acceptance criteria.
- Prompt includes multiple acceptance criteria.
- Acceptance criteria include validation or review expectations.

**Issues:**
- No issues recorded.

**Improvement Suggestions:**
- No improvement suggestions recorded.

### Evaluation for EP2

- Score: 100/100
- Ready to use: True

**Strengths:**
- Prompt starts with senior role framing.
- Prompt includes all required structure sections.
- Prompt has enough detail for engineering use.
- Prompt names the target role.
- Prompt identifies target AI coding tools.
- Prompt is tied to related plan phases.
- Prompt purpose is reflected in the prompt text.
- Prompt includes project-specific metadata.
- Prompt includes technical scope.
- Prompt includes meaningful constraints.
- Prompt references risk handling.
- Prompt references implementation tasks.
- Prompt preserves the product boundary.
- Prompt includes an Expected Output section.
- Prompt is positioned for external AI coding tools.
- Prompt keeps engineer review in the workflow.
- Prompt describes the expected deliverable type.
- Prompt includes an Acceptance Criteria section.
- Prompt includes meaningful acceptance criteria.
- Prompt includes multiple acceptance criteria.
- Acceptance criteria include validation or review expectations.

**Issues:**
- No issues recorded.

**Improvement Suggestions:**
- No improvement suggestions recorded.

### Evaluation for EP3

- Score: 100/100
- Ready to use: True

**Strengths:**
- Prompt starts with senior role framing.
- Prompt includes all required structure sections.
- Prompt has enough detail for engineering use.
- Prompt names the target role.
- Prompt identifies target AI coding tools.
- Prompt is tied to related plan phases.
- Prompt purpose is reflected in the prompt text.
- Prompt includes project-specific metadata.
- Prompt includes technical scope.
- Prompt includes meaningful constraints.
- Prompt references risk handling.
- Prompt references implementation tasks.
- Prompt preserves the product boundary.
- Prompt includes an Expected Output section.
- Prompt is positioned for external AI coding tools.
- Prompt keeps engineer review in the workflow.
- Prompt describes the expected deliverable type.
- Prompt includes an Acceptance Criteria section.
- Prompt includes meaningful acceptance criteria.
- Prompt includes multiple acceptance criteria.
- Acceptance criteria include validation or review expectations.

**Issues:**
- No issues recorded.

**Improvement Suggestions:**
- No improvement suggestions recorded.

### Evaluation for EP4

- Score: 100/100
- Ready to use: True

**Strengths:**
- Prompt starts with senior role framing.
- Prompt includes all required structure sections.
- Prompt has enough detail for engineering use.
- Prompt names the target role.
- Prompt identifies target AI coding tools.
- Prompt is tied to related plan phases.
- Prompt purpose is reflected in the prompt text.
- Prompt includes project-specific metadata.
- Prompt includes technical scope.
- Prompt includes meaningful constraints.
- Prompt references risk handling.
- Prompt references implementation tasks.
- Prompt preserves the product boundary.
- Prompt includes an Expected Output section.
- Prompt is positioned for external AI coding tools.
- Prompt keeps engineer review in the workflow.
- Prompt describes the expected deliverable type.
- Prompt includes an Acceptance Criteria section.
- Prompt includes meaningful acceptance criteria.
- Prompt includes multiple acceptance criteria.
- Acceptance criteria include validation or review expectations.

**Issues:**
- No issues recorded.

**Improvement Suggestions:**
- No improvement suggestions recorded.

### Evaluation for EP5

- Score: 100/100
- Ready to use: True

**Strengths:**
- Prompt starts with senior role framing.
- Prompt includes all required structure sections.
- Prompt has enough detail for engineering use.
- Prompt names the target role.
- Prompt identifies target AI coding tools.
- Prompt is tied to related plan phases.
- Prompt purpose is reflected in the prompt text.
- Prompt includes project-specific metadata.
- Prompt includes technical scope.
- Prompt includes meaningful constraints.
- Prompt references risk handling.
- Prompt references implementation tasks.
- Prompt preserves the product boundary.
- Prompt includes an Expected Output section.
- Prompt is positioned for external AI coding tools.
- Prompt keeps engineer review in the workflow.
- Prompt describes the expected deliverable type.
- Prompt includes an Acceptance Criteria section.
- Prompt includes meaningful acceptance criteria.
- Prompt includes multiple acceptance criteria.
- Acceptance criteria include validation or review expectations.

**Issues:**
- No issues recorded.

**Improvement Suggestions:**
- No improvement suggestions recorded.

### Evaluation for EP6

- Score: 100/100
- Ready to use: True

**Strengths:**
- Prompt starts with senior role framing.
- Prompt includes all required structure sections.
- Prompt has enough detail for engineering use.
- Prompt names the target role.
- Prompt identifies target AI coding tools.
- Prompt is tied to related plan phases.
- Prompt purpose is reflected in the prompt text.
- Prompt includes project-specific metadata.
- Prompt includes technical scope.
- Prompt includes meaningful constraints.
- Prompt references risk handling.
- Prompt references implementation tasks.
- Prompt preserves the product boundary.
- Prompt includes an Expected Output section.
- Prompt is positioned for external AI coding tools.
- Prompt keeps engineer review in the workflow.
- Prompt describes the expected deliverable type.
- Prompt includes an Acceptance Criteria section.
- Prompt includes meaningful acceptance criteria.
- Prompt includes multiple acceptance criteria.
- Acceptance criteria include validation or review expectations.

**Issues:**
- No issues recorded.

**Improvement Suggestions:**
- No improvement suggestions recorded.
