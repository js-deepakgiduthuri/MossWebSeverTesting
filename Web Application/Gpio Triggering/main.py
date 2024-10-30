from flask import Flask
import time
import gpiod

app = Flask(__name__)


def list_chips_and_pins():  #This function is not needed and not used in this project,this lists out all the gpio pins on the board
    for chip in gpiod.chip_iter():
        print(f"{chip.label}\t{chip.name}")
        for line in chip.get_all_lines():
            print(f"\t{line.offset}\t{line.name}\t{line.consumer}")

def set_line_state(line, state):
    gpioline = gpiod.find_line(line)
    if gpioline is None:
        print("Invalid line name.")
        return
    config = gpiod.line_request()
    config.consumer = "GPIO sample"
    config.request_type = gpiod.line_request.DIRECTION_OUTPUT
    gpioline.request(config, 1 if state else 0)


@app.route('/to_turn_on', methods=['GET'])
def turn_on_function():
    line = "SODIMM_54"  # Replace with your line name
    try:
        set_line_state(line, True)
        time.sleep(2)
        set_line_state(line, False)
        time.sleep(1)
        set_line_state(line, True)
        time.sleep(5)
        return "GPIO Script Executed Successfully", 200
    except Exception as e:
        return str(e), 500


@app.route('/to_turn_off', methods=['GET'])
def turn_off_function():
    line = "SODIMM_54"  # Replace with your line name
    try:
        set_line_state(line, True)
        time.sleep(2)
        set_line_state(line, False)
        time.sleep(2)
        set_line_state(line, True)
        time.sleep(2)
        set_line_state(line, False)
        time.sleep(5)
        return "GPIO Script Executed Successfully", 200
    except Exception as e:
        return str(e), 500


if __name__ == "__main__":
    app.run(port=5002, host='0.0.0.0')
