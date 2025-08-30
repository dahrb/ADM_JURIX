# ADM Web Application

This is a web-based user interface for the Argumentation Decision Framework (ADM) tool that replicates the exact functionality of the command line interface (`UI.py`).

## Features

The web app provides the same functionality as the CLI:

- **Domain Loading**: Load predefined domains (Wild Animals, Academic Research)
- **Question Processing**: Handle all question types:
  - Yes/No questions
  - Multiple choice questions
  - Question instantiators
  - Algorithmic BLFs
  - Sub-ADM evaluations
  - Evaluation BLFs
- **Case Building**: Build cases by answering questions
- **Case Evaluation**: Automatically evaluate cases using the ADF logic
- **Visualization**: Generate and display domain graphs
- **Real-time Updates**: See case status and progress in real-time

## Installation

1. Ensure you have the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. The web app uses the existing `MainClasses.py` and domain files without modification.

## Running the Web App

1. Start the web application:
   ```bash
   python web_app.py
   ```

2. Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

## Usage

### 1. Domain Selection
- Choose between "Wild Animals" and "Academic Research" domains
- Click "Load Selected Domain" to initialize the domain

### 2. Domain Operations
- **Start Query**: Begin answering questions to build a case
- **Visualize Domain**: Generate and view the domain graph
- **Back to Domains**: Return to domain selection

### 3. Query Process
- Answer questions one by one as they appear
- Questions are presented in the same order as the CLI
- All question types are supported:
  - **Yes/No**: Click Yes or No buttons
  - **Multiple Choice**: Select from available options
  - **Algorithmic**: Enter required inputs
  - **Sub-ADM**: Automatically processed
  - **Evaluation**: Automatically processed

### 4. Case Status
- View current case factors in real-time
- See progress as you answer questions
- Monitor which factors have been accepted/rejected

### 5. Results
- After completing all questions, view the evaluation results
- See the final case outcome and statements

## Architecture

### WebUI Class
The `WebUI` class mirrors the CLI functionality:
- `load_wild_animals_domain()`: Load Wild Animals domain
- `load_academic_research_domain()`: Load Academic Research domain
- `get_next_question()`: Get the next question to ask
- `process_answer()`: Process user answers and update case
- `evaluate_case()`: Evaluate the completed case
- `get_visualization()`: Generate domain visualization

### Flask Routes
- `/`: Main page
- `/load_domain`: Load a domain
- `/start_query`: Start querying the domain
- `/get_question`: Get next question
- `/submit_answer`: Submit answer to question
- `/visualize`: Generate visualization
- `/get_case_status`: Get current case status

### Frontend
- Modern, responsive HTML/CSS/JavaScript interface
- Real-time updates without page refresh
- Support for all question types
- Progress tracking and case status display

## Question Types Supported

1. **Regular Questions**: Yes/No questions for base-level factors
2. **Question Instantiators**: Multiple choice questions that create BLFs
3. **Algorithmic BLFs**: Questions that run algorithms based on user input
4. **Sub-ADM BLFs**: Questions that evaluate sub-ADMs for multiple items
5. **Evaluation BLFs**: Questions that automatically evaluate based on previous results
6. **Dependent BLFs**: Questions that inherit facts from other nodes

## Differences from CLI

- **Input Collection**: Web forms instead of command line input
- **Sub-ADM Handling**: Simplified for web interface (simulated evaluation)
- **Real-time Updates**: Case status updates as you progress
- **Visual Interface**: Modern web UI instead of text-based interface

## Testing

Run the test script to verify functionality:
```bash
python test_web_app.py
```

## Troubleshooting

- **Port Already in Use**: Change the port in `web_app.py` if 5000 is occupied
- **Domain Loading Errors**: Ensure all domain files are present and importable
- **Visualization Issues**: Check that `pydot` and Graphviz are properly installed

## Future Enhancements

- **User Authentication**: Add user accounts and case history
- **Case Management**: Save and load previous cases
- **Advanced Sub-ADM**: Full interactive sub-ADM evaluation
- **Export Options**: Export results to various formats
- **Mobile Optimization**: Better mobile device support

## Technical Notes

- The web app maintains the exact same logic flow as the CLI
- All question processing follows the same order and rules
- Case evaluation uses the same ADF logic
- Visualization generates identical graphs to the CLI version
- No modifications to existing domain files or MainClasses.py are required

