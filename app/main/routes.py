from flask import render_template, Blueprint

main = Blueprint('main', __name__)

lista=[
    {
        'item1': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Aspernatur esse illum iusto natus vitae? Aspernatur dolores expedita iure iusto nam recusandae voluptas? Aspernatur necessitatibus nobis perferendis sit veritatis voluptatum? Doloremque?'
    },
    {
        'item1': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Aspernatur esse illum iusto natus vitae? Aspernatur dolores expedita iure iusto nam recusandae voluptas? Aspernatur necessitatibus nobis perferendis sit veritatis voluptatum? Doloremque?'
    }
]


@main.route('/')
@main.route('/home')
def home():
    return render_template('home.html', title='Home', list=lista), 200