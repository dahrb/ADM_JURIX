# ADM Web UI - Modern Interface for Argumentation Decision Framework

This project provides a modern, responsive web-based user interface for the ADM (Argumentation Decision Framework) tool, replacing the command-line interface with an intuitive web application.

## 🚀 Features

### Modern Web Interface
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Beautiful UI**: Modern gradient backgrounds, smooth animations, and intuitive navigation
- **Interactive Elements**: Hover effects, smooth transitions, and visual feedback

### Enhanced User Experience
- **Progress Tracking**: Visual progress bar showing completion status
- **Question Types**: Support for multiple question types:
  - Question Instantiators
  - Simple Yes/No questions
  - Algorithmic questions with text inputs
  - Sub-ADM evaluations
- **Real-time Updates**: Dynamic question loading and answer processing

### Advanced Functionality
- **Session Management**: Create, manage, and resume evaluation sessions
- **Visual Results**: Interactive graph visualization with zoom and download capabilities
- **Case Summary**: Clear presentation of accepted factors and evaluation results
- **Graph Export**: Download decision network visualizations as PNG files

## 🛠️ Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Quick Start
1. **Clone or navigate to the project directory**
   ```bash
   cd /path/to/ADM_JURIX
   ```

2. **Run the startup script**
   ```bash
   python run_web_ui.py
   ```
   
   The script will automatically:
   - Check for required dependencies
   - Install missing packages if needed
   - Start the web server

3. **Access the interface**
   Open your web browser and navigate to: `http://localhost:5000`

### Manual Installation
If you prefer to install dependencies manually:

```bash
pip install -r requirements.txt
python web_ui.py
```

## 📱 Using the Web Interface

### 1. Landing Page
- **Start New Session**: Begin a new ADM evaluation
- **Feature Overview**: Learn about the tool's capabilities
- **Modern Design**: Beautiful gradient background with feature cards

### 2. Evaluation Process
- **Question Flow**: Answer questions step-by-step to build your case
- **Progress Tracking**: Visual progress bar and question counter
- **Question Types**: Different interfaces for various question types
- **Smart Navigation**: Automatic progression through the evaluation

### 3. Results Page
- **Case Summary**: Overview of all accepted factors
- **Evaluation Results**: Detailed analysis outcomes
- **Graph Visualization**: Interactive decision network diagram
- **Export Options**: Download graphs and start new sessions

## 🔧 Technical Details

### Architecture
- **Backend**: Flask web framework with Flask-SocketIO
- **Frontend**: Modern HTML5, CSS3, and JavaScript
- **Styling**: Bootstrap 5 with custom CSS variables
- **Icons**: Font Awesome for consistent iconography

### File Structure
```
ADM_JURIX/
├── web_ui.py              # Main Flask application
├── run_web_ui.py          # Startup script
├── requirements.txt        # Python dependencies
├── templates/             # HTML templates
│   ├── index.html         # Landing page
│   ├── evaluation.html    # Question interface
│   └── results.html       # Results display
├── MainClasses.py         # ADM core classes
├── inventive_step_ADM.py  # ADM domain definition
└── README_WEB_UI.md       # This file
```

### Dependencies
- **Flask**: Web framework
- **Flask-SocketIO**: Real-time communication
- **pydot**: Graph visualization
- **pythonds**: Data structures
- **Additional**: Various supporting packages

## 🎯 Question Types Supported

### 1. Question Instantiators
- Multiple choice questions that instantiate BLFs
- Factual ascription support
- Dynamic BLF creation

### 2. Simple Questions
- Yes/No questions for basic factors
- Clear visual feedback
- Immediate progression

### 3. Algorithmic Questions
- Text input fields for complex data
- Algorithmic processing
- Validation and error handling

### 4. Sub-ADM Evaluation
- Automatic sub-ADM processing
- Complex dependency handling
- Visual representation in graphs

## 🎨 Customization

### Styling
The interface uses CSS custom properties for easy theming:
```css
:root {
    --primary-color: #2c3e50;
    --secondary-color: #3498db;
    --success-color: #27ae60;
    --accent-color: #e74c3c;
}
```

### Layout
- Responsive grid system
- Mobile-first design
- Flexible component sizing

## 🚀 Running in Production

For production deployment, consider:

1. **WSGI Server**: Use Gunicorn or uWSGI
2. **Environment Variables**: Set `FLASK_ENV=production`
3. **Security**: Configure proper secret keys and HTTPS
4. **Scaling**: Use Redis for session storage

Example production command:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 web_ui:app
```

## 🔍 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Find process using port 5000
   lsof -i :5000
   # Kill the process
   kill -9 <PID>
   ```

2. **Missing Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Template Errors**
   - Ensure `templates/` directory exists
   - Check file permissions
   - Verify Jinja2 installation

4. **Graph Generation Issues**
   - Install Graphviz system package
   - Check pydot installation
   - Verify file write permissions

### Debug Mode
The interface runs in debug mode by default. For production, modify `web_ui.py`:
```python
socketio.run(app, debug=False, host='0.0.0.0', port=5000)
```

## 📊 Performance Considerations

- **Session Management**: In-memory sessions (consider Redis for production)
- **Graph Generation**: Cached visualization results
- **Responsive Design**: Optimized for various screen sizes
- **Loading States**: Visual feedback during processing

## 🤝 Contributing

To enhance the web interface:

1. **Frontend**: Modify HTML templates and CSS
2. **Backend**: Extend Flask routes and logic
3. **Styling**: Update CSS variables and components
4. **Functionality**: Add new question types or features

## 📝 License

This web interface is part of the ADM project and follows the same licensing terms.

## 🆘 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the existing command-line interface for reference
3. Examine the Flask application logs
4. Verify all dependencies are properly installed

---

**Enjoy using the modern ADM Web Interface!** 🎉
