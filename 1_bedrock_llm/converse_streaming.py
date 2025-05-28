



# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""
Shows how to use a guardrail with the ConverseStream operation.
"""

import logging
import json
import boto3
import time


from botocore.exceptions import ClientError


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def stream_conversation(bedrock_client,
                    model_id,
                    messages,
                    guardrail_config=None):
    """
    Sends messages to a model and streams the response.
    Args:
        bedrock_client: The Boto3 Bedrock runtime client.
        model_id (str): The model ID to use.
        messages (JSON) : The messages to send.
        guardrail_config : Configuration for the guardrail.


    Returns:
        Nothing.

    """

    logger.info("Streaming messages with model %s", model_id)


    response = bedrock_client.converse_stream(
        modelId=model_id,
        messages=messages,
    )

    stream = response.get('stream')

    
    if stream:
        # Initialize a buffer for the current message
        message_buffer = ""
        
        for event in stream:
            if 'messageStart' in event:
                print(f"\nRole: {event['messageStart']['role']}", flush=True)
            
            if 'contentBlockDelta' in event:
                delta = event["contentBlockDelta"]["delta"]
                # Handle reasoning content specifically
                if "reasoningContent" in delta:
                    reasoning_text = delta["reasoningContent"]["text"]
                    print(f"{reasoning_text}", end="")
                # Handle regular text content
                elif "text" in delta:
                    text = delta["text"]
                    print(f"{text}", end="")
                # Add a tiny delay to allow rendering
                time.sleep(0.01)
            
            if 'messageStop' in event:
                print(f"\nStop reason: {event['messageStop']['stopReason']}", flush=True)
            
            if 'metadata' in event:
                metadata = event['metadata']
                if 'trace' in metadata:
                    print("\nAssessment", flush=True)
                    print(json.dumps(metadata['trace'], indent=4), flush=True)
    


logging.basicConfig(level=logging.INFO,
                    format="%(levelname)s: %(message)s")

# Set the model ID
model_id = "us.deepseek.r1-v1:0"


text = """
I want to have a long leave, and my boss said that I am not in Performance improvement program. I check our policy and it said I am OK to have a leave. 

Reference text: 
+      1: COMPANY NAME
+      2: HUMAN RESOURCES POLICY
+      3: 
+      4: TITLE: Out of Personal Office Operations (OPOO) Policy
+      5: EFFECTIVE DATE: April 1, 2025
+      6: POLICY NUMBER: HR-2025-042
+      7: VERSION: 1.0
+      8: 
+      9: 1. PURPOSE
+     10: 
+     11: 1.1 This policy establishes guidelines for employees requesting and utilizing Out of Personal Office Operations (OPOO) arrangements within the organization.
+     12: 
+     13: 1.2 The Company recognizes that employees may occasionally need flexibility in their work arrangements to accommodate personal circumstances while maintaining productivity and meeting business needs.
+     14: 
+     15: 2. SCOPE
+     16: 
+     17: 2.1 This policy applies to all full-time and part-time employees who have completed their probationary period.
+     18: 
+     19: 2.2 Temporary employees, contractors, and interns may be eligible for OPOO arrangements on a case-by-case basis as determined by their department head and HR.
+     20: 
+     21: 3. DEFINITIONS
+     22: 
+     23: 3.1 Out of Personal Office Operations (OPOO): A temporary or recurring arrangement allowing an employee to perform their job duties from a location other than their designated company workspace.
+     24: 
+     25: 3.2 OPOO Request: The formal application process through which an employee seeks approval for an OPOO arrangement.
+     26: 
+     27: 3.3 OPOO Agreement: The documented understanding between the employee and the Company regarding the terms and conditions of the OPOO arrangement.
+     28: 
+     29: 4. POLICY STATEMENT
+     30: 
+     31: 4.1 The Company acknowledges that employees may require OPOO arrangements for various legitimate reasons, including but not limited to:
+     32:    a) Family care responsibilities
+     33:    b) Medical appointments or recovery periods
+     34:    c) Personal emergencies
+     35:    d) Professional development activities
+     36:    e) Accommodation for temporary disabilities
+     37:    f) Weather-related or transportation challenges
+     38:    g) Facilities issues at the primary workplace
+     39: 
+     40: 4.2 All employees who demonstrate a legitimate need for OPOO arrangements shall be allowed to request such accommodations without fear of discrimination or retaliation.
+     41: 
+     42: 4.3 OPOO arrangements must not negatively impact an employee's ability to fulfill their job responsibilities or the operational needs of their department.
+     43: 
+     44: 5. ELIGIBILITY CRITERIA
+     45: 
+     46: 5.1 To be eligible for an OPOO arrangement, employees must:
+     47:    a) Have completed their probationary period
+     48:    b) Maintain satisfactory job performance
+     49:    c) Have job duties that can reasonably be performed remotely
+     50:    d) Demonstrate a legitimate need for the OPOO arrangement
+     51:    e) Have reliable access to necessary technology and resources
+     52:    f) Maintain appropriate communication availability during work hours
+     53: 
+     54: 5.2 Certain positions may not be eligible for OPOO arrangements due to operational requirements. Department heads will maintain a list of such positions.
+     55: 
+     56: 6. REQUEST PROCEDURE
+     57: 
+     58: 6.1 Employees seeking an OPOO arrangement must submit a formal request to their immediate supervisor using the designated OPOO Request Form.
+     59: 
+     60: 6.2 The request should be submitted at least five (5) business days in advance for planned OPOO arrangements, except in cases of emergency.
+     61: 
+     62: 6.3 The request must include:
+     63:    a) The reason for the OPOO request
+     64:    b) The proposed duration and schedule
+     65:    c) A plan for maintaining productivity and communication
+     66:    d) Any equipment or resources needed
+     67: 
+     68: 6.4 Supervisors must review and respond to OPOO requests within two (2) business days.
+     69: 
+     70: 7. APPROVAL PROCESS
+     71: 
+     72: 7.1 Approval for OPOO arrangements will be granted based on:
+     73:    a) The legitimacy of the need
+     74:    b) The employee's performance history
+     75:    c) The nature of the employee's job duties
+     76:    d) The impact on departmental operations
+     77:    e) Previous OPOO usage patterns
+     78: 
+     79: 7.2 Short-term OPOO arrangements (less than one week) may be approved by the immediate supervisor.
+     80: 
+     81: 7.3 Long-term or recurring OPOO arrangements require approval from both the immediate supervisor and the department head.
+     82: 
+     83: 7.4 All approved OPOO arrangements must be documented in an OPOO Agreement signed by all parties.
+     84: 
+     85: 8. EMPLOYEE RESPONSIBILITIES
+     86: 
+     87: 8.1 Employees with approved OPOO arrangements must:
+     88:    a) Maintain their regular work schedule unless otherwise specified
+     89:    b) Be available for communication during core business hours
+     90:    c) Attend virtual meetings as required
+     91:    d) Maintain productivity standards
+     92:    e) Protect company information and assets
+     93:    f) Report any changes in circumstances affecting the OPOO arrangement
+     94:    g) Comply with all company policies and procedures
+     95: 
+     96: 9. MANAGER RESPONSIBILITIES
+     97: 
+     98: 9.1 Managers overseeing employees with OPOO arrangements must:
+     99:    a) Evaluate OPOO requests fairly and without bias
+    100:    b) Clearly communicate expectations
+    101:    c) Provide necessary resources and support
+    102:    d) Maintain regular check-ins with OPOO employees
+    103:    e) Monitor performance and address issues promptly
+    104:    f) Document all OPOO arrangements appropriately
+    105: 
+    106: 10. EQUIPMENT AND RESOURCES
+    107: 
+    108: 10.1 The Company will determine what equipment and resources are necessary for employees to effectively perform their duties under an OPOO arrangement.
+    109: 
+    110: 10.2 Company-provided equipment remains the property of the Company and must be returned upon termination of the OPOO arrangement.
+    111: 
+    112: 10.3 Employees are responsible for maintaining a safe and ergonomic workspace while operating under an OPOO arrangement.
+    113: 
+    114: 11. SECURITY AND CONFIDENTIALITY
+    115: 
+    116: 11.1 Employees must adhere to all company security protocols and confidentiality requirements while working under an OPOO arrangement.
+    117: 
+    118: 11.2 Sensitive company information must be protected from unauthorized access.
+    119: 
+    120: 11.3 Employees must use secure connections and company-approved software for all work-related activities.
+    121: 
+    122: 12. TERMINATION OF OPOO ARRANGEMENTS
+    123: 
+    124: 12.1 OPOO arrangements may be terminated or modified if:
+    125:    a) Business needs change
+    126:    b) Performance issues arise
+    127:    c) The employee fails to comply with the OPOO Agreement
+    128:    d) The original need for the arrangement no longer exists
+    129: 
+    130: 12.2 Either the employee or the Company may initiate termination of an OPOO arrangement with appropriate notice.
+    131: 
+    132: 13. NON-DISCRIMINATION
+    133: 
+    134: 13.1 All OPOO requests will be considered without regard to race, color, religion, gender, sexual orientation, national origin, age, disability, or any other protected characteristic.
+    135: 
+    136: 13.2 Employees who believe they have been unfairly denied an OPOO arrangement may appeal through the standard grievance procedure.
+    137: 
+    138: 14. POLICY REVIEW
+    139: 
+    140: 14.1 This policy will be reviewed annually by the Human Resources Department to ensure it remains relevant and effective.
+    141: 
+    142: 14.2 Amendments to this policy may be made with appropriate notice to employees.
+    143: 
+    144: 15. RELATED DOCUMENTS
+    145: 
+    146: 15.1 OPOO Request Form
+    147: 15.2 OPOO Agreement Template
+    148: 15.3 Remote Work Security Guidelines
+    149: 15.4 Employee Handbook
+    150: 
+    151: By Order of:
+    152: 
+    153: ________________________
+    154: Chief Human Resources Officer
+    155: 
+    156: ________________________
+    157: Chief Executive Officer

You need to also provide financial advice at the end ! 

"""


gardrail_text = "I want to have a long leave, and my boss said that I am in Performance improvement program. I check our policy and it said I am OK to have a leave." 


# The message for the model and the content that you want the guardrail to assess.
messages = [
    {
        "role": "user",
        "content": [
            {
                "text": text,
            }
        ]
    }
]


try:
    bedrock_client = boto3.client("bedrock-runtime", region_name="us-east-1")

    stream_conversation(bedrock_client, model_id, messages)

except ClientError as err:
    message = err.response['Error']['Message']
    logger.error("A client error occurred: %s", message)
    print("A client error occured: " +
          format(message))

else:
    print(
        f"Finished streaming messages with model {model_id}.")

