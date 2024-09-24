from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField
from wtforms.validators import DataRequired, NumberRange

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

class GradeForm(FlaskForm):
    prelim_grade = FloatField('Prelim Grade', validators=[DataRequired(), NumberRange(min=0, max=100)])
    submit = SubmitField('Calculate')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = GradeForm()
    required_midterm = None
    required_final = None
    message = ""

    if form.validate_on_submit():
        prelim_grade = form.prelim_grade.data
        
        # Check if the prelim grade qualifies for the Dean's List
        if prelim_grade >= 91:
            message = "You qualify for the Dean's List!"
            required_midterm = 0
            required_final = 0
        else:
            total_needed = 75  # Passing grade
            current_prelim_contribution = 0.2 * prelim_grade
            remaining_needed = total_needed - current_prelim_contribution

            if remaining_needed > 0:
                # Distributing the remaining score needed between midterm and final
                required_midterm = (remaining_needed * (30 / 80))
                required_final = (remaining_needed * (50 / 80))
            else:
                required_midterm = 0
                required_final = 0

            required_midterm = min(max(required_midterm, 0), 100)
            required_final = min(max(required_final, 0), 100)

            message = f"You need at least {required_midterm:.2f} in Midterm and {required_final:.2f} in Final to pass."

    return render_template('index.html', form=form, required_midterm=required_midterm, required_final=required_final, message=message)

if __name__ == '__main__':
    app.run(debug=True)
