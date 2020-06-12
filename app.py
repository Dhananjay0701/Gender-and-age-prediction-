from flask import Flask, render_template, request, Response
import model
app = Flask(__name__)
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods = ['GET', 'POST'])
def register(self):
    self.link = request.form.get('link')

@app.route('/video_feed')
def video_feed(self):
    """Video streaming route. Put this in the src attribute of an img tag."""
    model.video.link(self.link)
    age_net, gender_net = model.video.caffe_models()
    return Response(model.video.video_detector(age_net, gender_net),mimetype='multipart/x-mixed-replace; boundary=frame')


    

if __name__ == "__main__":
    app.run(debug = True)
