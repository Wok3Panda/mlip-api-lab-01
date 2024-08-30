from flask import Flask, request, jsonify, render_template
from analyze import read_image

from flasgger import Swagger, swag_from

app = Flask(__name__, template_folder='templates')

# Initialize Swagger
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'lab01doc',
            "route": '/lab01doc.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/doc/"
}

swagger = Swagger(app, config=swagger_config)


@app.route("/")
def home():
    return render_template('index.html')


# API at /api/v1/analysis/ 
@app.route("/api/v1/analysis/", methods=['GET'])
@swag_from({
    'tags': ['Image Analysis'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'uri': {
                        'type': 'string',
                        'description': 'The URI of the image to analyze',
                        'example': 'https://miro.medium.com/v2/resize:fit:1400/1*0KFB17_NGTPB0XWyc4BSgQ.jpeg'
                    }
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Text extracted successfully from the image',
            'schema': {
                'type': 'object',
                'properties': {
                    'text': {
                        'type': 'string',
                        'example': 'Detected text from the image'
                    }
                }
            }
        },
        400: {'description': 'Missing URI in JSON'},
        500: {'description': 'Error in processing'}
    }
})


def analysis():
    # Try to get the URI from the JSON
    try:
        get_json = request.get_json()
        image_uri = get_json['uri']
    except:
        return jsonify({'error': 'Missing URI in JSON'}), 400
    
    # Try to get the text from the image
    try:
        res = read_image(image_uri)
        
        response_data = {
            "text": res
        }
    
        return jsonify(response_data), 200
    except:
        return jsonify({'error': 'Error in processing'}), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)