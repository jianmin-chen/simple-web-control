import socket
from motor_test import test_motor
import time
from pymavlink import mavutil


def arm_rov(mav_connection):
    """
    Arm the ROV, wait for confirmation
    """
    mav_connection.arducopter_arm()
    print("Waiting for the vehicle to arm")
    mav_connection.motors_armed_wait()
    print("Armed!")


def disarm_rov(mav_connection):
    """
    Disarm the ROV, wait for confirmation
    """
    mav_connection.arducopter_disarm()
    print("Waiting for the vehicle to disarm")
    mav_connection.motors_disarmed_wait()
    print("Disarmed!")


def choreography(mav_connection):
    """
    Choreography
    """

    for i in range(6):
        # Do a flower of sorts
        run_motors_timed(
            mav_connection, seconds=10, motor_settings=[70, 80, 0, 70, 0, 0]
        )
        run_motors_timed(
            mav_connection, seconds=5, motor_settings=[100, 100, 0, 0, 0, 0]
        )
        run_motors_timed(
            mav_connection, seconds=10, motor_settings=[70, 80, 0, 70, 0, 0]
        )
    run_motors_timed(
        mav_connection, seconds=20, motor_settings=[100, 50, 100, 50, 0, 0]
    )


def run_motors_timed(mav_connection, seconds: int, motor_settings: list) -> None:
    """
    Run the motors for a set time
    :param mav_connection: The mavlink connection
    :param time: The time to run the motors
    :param motor_settings: The motor settings, a list of 6 values -100 to 100
    :return: None
    """
    step = 0
    while step < seconds:
        for i in range(len(motor_settings)):
            test_motor(
                mav_connection=mav_connection, motor_id=i, power=motor_settings[i]
            )
        time.sleep(0.2)
        step += 0.2


if __name__ == "__main__":
    ####
    # Initialize ROV
    ####
    mav_connection = mavutil.mavlink_connection("udpin:0.0.0.0:14550")
    mav_connection.wait_heartbeat()
    # Arm the ROV and wait for confirmation
    arm_rov(mav_connection)

    ####
    # Run choreography
    ####
    # choreography(mav_connection)

    # stop
    # run_motors_timed(mav_connection, seconds=5, motor_settings=[0, 0, 0, 0, 0, 0])

    # Open TCP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Start listening on port
    port = 5001
    s.bind(("0.0.0.0", port))
    backlog = 10
    s.listen(backlog)
    print("Socket created")

    connection, address = s.accept()
    while True:
        data = connection.recv(1024).decode("ascii")
        try:
            data = [float(arg) for arg in data.split(" ")]
            if len(data) != 7:
                raise Exception("Not enough arguments")
            print("Running with arguments: ", data)
            run_motors_timed(
                mav_connection=mav_connection, seconds=data[0], motor_settings=data[1:]
            )
        except:
            # An error happened
            print("Error moving AUV")
            break

    disarm_rov(mav_connection)
    s.close()
