import json
import os
import cohere
from cohere import ClassifyExample
from dotenv import load_dotenv

load_dotenv()

def classify_emails(emails):
    with open('backend/examples.json', 'r') as f:
        examples_data = json.load(f)
    examples = [ClassifyExample(text=example['text'], label=example['label']) for example in examples_data]

    with open('backend/inputs.json', 'r') as f:
        inputs = json.load(f)

    
    COHERE_API_KEY = os.getenv('COHERE_API_KEY')
    co = cohere.Client(COHERE_API_KEY)

    try:
        # Classify the inputs
        response = co.classify(
            model='embed-english-v2.0',
            inputs=inputs,
            examples=examples
        )
        print("Classification request successful. Processing response...")
        
        cleaned_output = []
        
        for i, classification in enumerate(response.classifications):
            input_text = classification.input
            email_id = input_text.split(' ')[2]  # Extract the email ID
            subject = input_text.split('Subject: ')[1].split(' Sender: ')[0]  # Extract the subject
            prediction = classification.prediction
            
            
            email_body = inputs[i]  # Use the actual email body for the generate prompt
            
            #generate model
            generate_response = co.generate(
                model='command',
                prompt=f'Only extract the compnay name from the email, dont write anything extra and dont ask any questions only company name:\n\n{email_body}',
                max_tokens=40,
                temperature=0.4,
                k=0,
                stop_sequences=[],
                return_likelihoods='NONE'
            )
            
            company_name = generate_response.generations[0].text.strip()
            # Add to cleaned output with the company name
            cleaned_output.append({
                'email_id': email_id,
                'subject': subject,
                'classification': prediction,
                'company_name': company_name  # Include company name in the output
            })


        with open('backend/cleaned_classifications.json', 'w') as f:
            json.dump(cleaned_output, f, indent=4)
        
        print(cleaned_output)
        return cleaned_output

    except Exception as e:
        print(f"Error during classification: {e}")
        return []

if __name__ == '__main__':
    classify_emails([])  
