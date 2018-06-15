from car.vehicle import Vehicle
from car.config import load_config
from car.parts.camera import Webcam
from car.parts.engine import Engine
from car.parts.web_controller.web import LocalWebController
from car.parts.web_controller.prediction_caller import PredictionCaller
from car.parts.datastore import DatasetHandler


# Load default settings
cfg = load_config()

# Initialize the car
car = Vehicle(warm_up_seconds=cfg.WARM_UP_SECONDS)

# Add a webcam
cam = Webcam(pi_host=cfg.PI_HOSTNAME, name='camera', unit_test=False)
car.add(
    cam,
    outputs=['cam/image_array'],
    threaded=True)

# TODO: Figure out why drive mode takes 2 full seconds to send commands back to Tornado
# Add a local Tornado web server to receive commands
ctr = LocalWebController(name='server',pi_host=cfg.PI_HOSTNAME, port=cfg.WEB_UI_PORT)
car.add(
    ctr,
    inputs=['cam/image_array'],
    outputs=['user/angle', 'user/throttle', 'mode', 'recording'],
    threaded=True)
server_message = "You can now go to {host}:{port} to drive your car."
print(server_message.format(host=cfg.PI_HOSTNAME, port=cfg.WEB_UI_PORT))

# This shouldn't have to know if the model exists.
# It should return 0s if the model doesn't exist
# or if the model exists but simply isn't reachable
# Add prediction caller
prediction_caller = PredictionCaller(model_api=cfg.MODEL_API,name='ai')
car.add(
    prediction_caller,
    inputs=['cam/image_array'],
    outputs=['ai/angle', 'ai/throttle'],
    threaded=True)

# Add engine
engine_inputs =[
    'user/angle',
    'user/throttle',
    'ai/angle',
    'ai/throttle',
    'mode',
    'latency-brake']
engine = Engine(16, 18, 22, 19, 21, 23, name='engine', inputs=engine_inputs)
car.add(
    engine,
    inputs=engine_inputs,
    threaded=True)

# Add dataset to save data
recorded_inputs = [
    'cam/image_array',
    'user/angle',
    'user/throttle',
    'ai/angle',
    'ai/throttle',
    'mode',
    'latency-brake']
types = [
    'image_array',
    'float',
    'float',
    'float',
    'float',
    'str',
    'str']
dh = DatasetHandler(path=cfg.DATA_PATH)
print(cfg.DATA_PATH)
dataset = dh.new_dataset_writer(inputs=recorded_inputs, types=types)
dataset.set_name('dataset')
car.add(
    dataset,
    inputs=recorded_inputs,
    run_condition='recording')

car.start(
    rate_hz=cfg.DRIVE_LOOP_HZ,
    max_loop_count=cfg.MAX_LOOPS)
