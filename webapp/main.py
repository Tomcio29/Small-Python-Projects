from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from forms import DataForm
from flask_bootstrap import Bootstrap5

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///model.db'
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
db = SQLAlchemy(app)
Bootstrap5(app)


class DataModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pregnancies = db.Column(db.Float, nullable=False)
    glucose = db.Column(db.Float, nullable=False)
    blood_pressure = db.Column(db.Float, nullable=False)
    skin_thickness = db.Column(db.Float, nullable=False)
    insulin = db.Column(db.Float, nullable=False)
    bmi = db.Column(db.Float, nullable=False)
    diabetes_pedigree_function = db.Column(db.Float, nullable=False)
    age = db.Column(db.Float, nullable=False)
    outcome = db.Column(db.Integer, nullable=False)


@app.route('/')
def show_data():
    data_points = DataModel.query.all()
    return render_template('index.html', data_points=data_points)


@app.route('/add', methods=['GET', 'POST'])
def add_data():
    form = DataForm()
    if form.validate_on_submit():
        new_data = DataModel(
            pregnancies=form.pregnancies.data,
            glucose=form.glucose.data,
            blood_pressure=form.blood_pressure.data,
            skin_thickness=form.skin_thickness.data,
            insulin=form.insulin.data,
            bmi=form.bmi.data,
            diabetes_pedigree_function=form.diabetes_pedigree_function.data,
            age=form.age.data,
            outcome=form.outcome.data
        )
        db.session.add(new_data)
        db.session.commit()
        return redirect('/')
    return render_template('add.html', form=form)


@app.route('/delete/<int:record_id>', methods=['POST'])
def delete_data(record_id):
    if request.method == 'POST':
        data_point = DataModel.query.get(record_id)
        if data_point:
            db.session.delete(data_point)
            db.session.commit()
            return redirect('/')
        else:
            return render_template('404.html'), 404


@app.route('/api/data', methods=['GET'])
def get_data():
    data_points = DataModel.query.all()
    data_list = [
        {
            'id': data.id,
            'pregnancies': data.pregnancies,
            'glucose': data.glucose,
            'blood_pressure': data.blood_pressure,
            'skin_thickness': data.skin_thickness,
            'insulin': data.insulin,
            'bmi': data.bmi,
            'diabetes_pedigree_function': data.diabetes_pedigree_function,
            'age': data.age,
            'outcome': data.outcome
        }
        for data in data_points
    ]
    return jsonify(data_list)


@app.route('/api/data', methods=['POST'])
def post_data():
    post_data = request.json
    required_fields = ['pregnancies', 'glucose', 'blood_pressure',
                       'skin_thickness', 'insulin', 'bmi',
                       'diabetes_pedigree_function', 'age', 'outcome']
    for field in required_fields:
        if field not in post_data or post_data[field] is None:
            return jsonify({'error': f'Missing value or field: {field}'}), 400

    numeric_fields = ['pregnancies', 'glucose', 'blood_pressure',
                      'skin_thickness', 'insulin', 'bmi',
                      'diabetes_pedigree_function', 'age']

    for field in numeric_fields:
        try:
            value = float(post_data[field])
            if value < 0:
                return jsonify({'error': f'Field {field} must be positive or zero'}), 400
            post_data[field] = value
        except ValueError:
            return jsonify({'error': f'Invalid data type in field: {field}'}), 400

    if post_data['outcome'] not in [0, 1]:
        return jsonify({'error': 'Invalid value for field: outcome. It must be 0 or 1'}), 400

    new_data = DataModel(**post_data)
    db.session.add(new_data)
    db.session.commit()
    return jsonify({'id': new_data.id})


@app.route('/api/data/<int:record_id>', methods=['DELETE'])
def api_delete_data(record_id):
    data = DataModel.query.get(record_id)
    if data:
        db.session.delete(data)
        db.session.commit()
        return jsonify({'id': record_id})
    return jsonify({'error': 'Record not found'}), 404


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
