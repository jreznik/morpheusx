import argparse
import sys
import hid

def main(args=sys.argv):
    
    parser = argparse.ArgumentParser(description='Playstation VR control utility')
    parser.add_argument('--on', help='Turn on PS VR, defaults to 3D mode, no tracking', action='store_true')
    parser.add_argument('--threed', help='Set 3D mode', action='store_true')
    parser.add_argument('--cinematic', help='Set cinematic mode', action='store_true')
    parser.add_argument('--off', help='Turn off PS VR', action='store_true')

    args = parser.parse_args()

    devices = hid.enumerate(0x054c, 0x09af) 

    device_path = ''

    for interface in devices:
        if interface['interface_number'] == 5:
            device_path = interface['path']
        
    ctl = hid.device(0x054c, 0x09af)

    ctl.open_path(device_path)

    if args.on:
        print "Turning PS VR on"
        mode = "3D" # default mode
    
        if args.threed and args.cinematic:
            print "Please select only one mode, defaulting to 3D mode"
            mode = "3D"
        else:
            if args.threed:
                print "...into 3D mode"
                mode = "3D"
    
            if args.cinematic:
                print "...into cinematic mode"
                mode = "cinematic"

        print mode
        ret = ctl.write([0x23, 0x00, 0xaa, 0x04, 0x01, 0x00, 0x00, 0x00])

        if ret > -1:
            print "Success"
    else:
        if args.off:
            if args.threed or args.cinematic:
                print "Off command does not take any arguments... Ignoring"

            print "Turning PS VR off"   
            
            ret = ctl.write([0x23, 0x00, 0xaa, 0x04, 0x00, 0x00, 0x00, 0x00])

            if ret > -1:
                print "Success"
        else:
            print "No command specified. --on or --off commands is required"

if __name__ == "__main__":
    main(sys.argv)
