#Author-RoTechnic and Ben Burke
#Description-Create Cycloid Shapes

import adsk.core, adsk.fusion, adsk.cam, traceback
import math

handlers = []

def drange(start, stop, step):
    r = start
    while r <= stop:
        yield r
        r += step

def cos(angle):
    return math.cos(math.radians(angle))

def sin(angle):
    return math.sin(math.radians(angle))

def calc_points_cycloid(angle, cycloid_base_radius, rolling_circle_radius, number_of_pins, contraction):
    x =  (cycloid_base_radius + rolling_circle_radius) * cos(angle)
    y =  (cycloid_base_radius + rolling_circle_radius) * sin(angle)

    return [
        x + (rolling_circle_radius - contraction) * cos(number_of_pins*angle),
        y + (rolling_circle_radius - contraction) * sin(number_of_pins*angle)
    ]

def calc_points_inverse_cycloid(angle, cycloid_base_radius, rolling_circle_radius, number_of_pins, contraction):
    x = (cycloid_base_radius - rolling_circle_radius) * math.cos(math.radians(angle))
    y = (cycloid_base_radius - rolling_circle_radius) * math.sin(math.radians(angle))

    return [
        x + (rolling_circle_radius - contraction) * math.cos(math.radians(number_of_pins * -angle)),
        y + (rolling_circle_radius - contraction) * math.sin(math.radians(number_of_pins * -angle))
    ]

def interpolate_curve(xy_coordinates, num_points):
    # Separate the x and y coordinates into separate lists
    x_coords, y_coords = zip(*xy_coordinates)

    # Calculate the cumulative distance along the curve
    distances = [0]
    total_distance = 0
    for i in range(1, len(x_coords)):
        dx = x_coords[i] - x_coords[i-1]
        dy = y_coords[i] - y_coords[i-1]
        segment_distance = ((dx**2) + (dy**2)) ** 0.5
        total_distance += segment_distance
        distances.append(total_distance)

    # Create a linearly spaced list of distances for the desired number of points
    target_distances = [i * total_distance / (num_points - 1) for i in range(num_points)]

    # Interpolate the x and y coordinates separately
    interpolated_x = []
    interpolated_y = []
    current_distance_index = 0
    for target_distance in target_distances:
        while distances[current_distance_index] < target_distance:
            current_distance_index += 1
            if current_distance_index >= len(distances) - 1:
                break

        if current_distance_index >= len(distances) - 1:
            break

        # Linear interpolation
        t = (target_distance - distances[current_distance_index-1]) / (distances[current_distance_index] - distances[current_distance_index-1])
        interpolated_x.append((1 - t) * x_coords[current_distance_index-1] + t * x_coords[current_distance_index])
        interpolated_y.append((1 - t) * y_coords[current_distance_index-1] + t * y_coords[current_distance_index])

    # Combine the interpolated x and y coordinates into a new list of XY coordinates
    interpolated_coordinates = list(zip(interpolated_x, interpolated_y))

    return interpolated_coordinates

def lines_to_points(lines):
    coords = []
    for line in lines:
        coords.append( 
            [ 
                [ line.startSketchPoint.geometry.x, line.startSketchPoint.geometry.y ], 
                [ line.endSketchPoint.geometry.x, line.endSketchPoint.geometry.y ] 
            ] )
    return coords

def mirror_points(lines, mirror_start=[0,0], mirror_end=[0,0]):
    mirrored_lines = []

    # Compute the angle of the mirror line
    angle = math.atan2(mirror_end[1] - mirror_start[1], mirror_end[0] - mirror_start[0])

    for line in lines:
        start_x, start_y = line[0]
        end_x, end_y = line[1]

        # Compute the vectors from the mirror line start point to the line start and end points
        start_vector = [start_x - mirror_start[0], start_y - mirror_start[1]]
        end_vector = [end_x - mirror_start[0], end_y - mirror_start[1]]

        # Compute the mirrored vectors
        start_mirrored_vector = [math.hypot(*start_vector) * math.cos(2 * angle - math.atan2(start_vector[1], start_vector[0])),
                                math.hypot(*start_vector) * math.sin(2 * angle - math.atan2(start_vector[1], start_vector[0]))]
        end_mirrored_vector = [math.hypot(*end_vector) * math.cos(2 * angle - math.atan2(end_vector[1], end_vector[0])),
                            math.hypot(*end_vector) * math.sin(2 * angle - math.atan2(end_vector[1], end_vector[0]))]

        # Compute the mirrored points by adding the mirrored vectors to the mirror line start point
        mirrored_start_x = mirror_start[0] + start_mirrored_vector[0]
        mirrored_start_y = mirror_start[1] + start_mirrored_vector[1]
        mirrored_end_x = mirror_start[0] + end_mirrored_vector[0]
        mirrored_end_y = mirror_start[1] + end_mirrored_vector[1]

        # Add the mirrored line to the new list
        mirrored_lines.append([[mirrored_start_x, mirrored_start_y], [mirrored_end_x, mirrored_end_y]])

    return mirrored_lines

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface

        # Get the CommandDefinitions collection.
        cmdDefs = ui.commandDefinitions

        # Create a button command definition.
        cycloidGeneratorButton = cmdDefs.addButtonDefinition('GenerateCycloidId', 
                                                   'Cycloid Generator', 
                                                   'Generate Cycloid Shapes')
        
        # Connect to the command created event.
        cycloidGeneratorCreated = CycloidGeneratorCommandCreatedEventHandler()
        cycloidGeneratorButton.commandCreated.add(cycloidGeneratorCreated)
        handlers.append(cycloidGeneratorCreated)
        
        # Execute the command.
        cycloidGeneratorButton.execute()
        
        # Keep the script running.
        adsk.autoTerminate(False)
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

# Event handler for the commandCreated event.
class CycloidGeneratorCommandCreatedEventHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        eventArgs = adsk.core.CommandCreatedEventArgs.cast(args)
        # Get the command
        cmd = eventArgs.command

        # Get the CommandInputs collection to create new command inputs.            
        inputs = cmd.commandInputs

        # Type        
        typeDropdown = inputs.addDropDownCommandInput(
            'typeDropdownId', 'Type', adsk.core.DropDownStyles.TextListDropDownStyle
        )
        typeDropdown.listItems.add('External', True)
        typeDropdown.listItems.add('Internal', False)

        # Complexity Slider
        # Set the step size and minimum/maximum values for the slider
        stepSize = 10
        minVal = 25
        maxVal = 105
        complexity = inputs.addIntegerSliderCommandInput(
            'complexityId',
            'Complexity',
            minVal,
            maxVal,
            False
        )
        complexity.spinStep = stepSize
        complexity.valueOne = 55
        
         # Add a number input for "Number of Pins"
        inputs.addValueInput(
            'pinsNumberInputId', 'Number of Pins', '', adsk.core.ValueInput.createByString('12')
        )

        # Add a number input for "Pin Radius"
        inputs.addValueInput(
            'pinRadiusInputId', 'Pin Radius (mm)', 'mm', adsk.core.ValueInput.createByString('5')
        )

        # Add a number input for "Pitch Radius"
        inputs.addValueInput(
            'pitchRadiusInputId', 'Pitch Radius (mm)', 'mm', adsk.core.ValueInput.createByString('30')
        )

        # Add a number input for "Contraction"
        inputs.addValueInput(
            'contractionInputId', 'Contraction (mm)', 'mm', adsk.core.ValueInput.createByString('0.5')
        )

        # Add a number input for "Contraction"
        inputs.addBoolValueInput('drawPinInputId', 'Draw Pin', True, '', False)

        # Connect to the execute event.
        onExecute = CycloidGeneratorCommandExecuteHandler()
        cmd.execute.add(onExecute)
        handlers.append(onExecute)

# Event handler for the execute event.
class CycloidGeneratorCommandExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        eventArgs = adsk.core.CommandEventArgs.cast(args) 
        inputs = eventArgs.command.commandInputs

        self.app = adsk.core.Application.get()
        self.product = self.app.activeProduct
        self.design = adsk.fusion.Design.cast(self.product)        
        self.ui  = self.app.userInterface
        
        #### Code Here
        self.shape_type = inputs.itemById('typeDropdownId').selectedItem.name
        self.complexity = int((inputs.itemById('complexityId').valueOne // 5)*5)
        self.complexity += 5 if self.complexity % 2 == 0 else 0
        self.number_of_pins = int(inputs.itemById('pinsNumberInputId').value)
        self.pin_radius = float(inputs.itemById('pinRadiusInputId').value)
        self.pitch_radius = float(inputs.itemById('pitchRadiusInputId').value)
        self.contraction = float(inputs.itemById('contractionInputId').value)
        self.draw_pin = bool(inputs.itemById('drawPinInputId').value)

        self.ui.messageBox(f"{self.shape_type} Eccentric Cycloid Shape Selected.\nPlease be patient as this may take a few minutes.\nPress OK to begin.", "Generating Geometry")

        self.generateGeometry(isInverse=bool("Internal" in self.shape_type), drawPin=self.draw_pin)

        # Force the termination of the command.
        adsk.terminate()
  
    def generateGeometry(self, isInverse=False, drawPin=False):
        try:
            # Get root component in this design
            rootComp = self.design.rootComponent

            # Create a new sketch on the xy plane.
            sketches = rootComp.sketches
            xyPlane = rootComp.xYConstructionPlane
            sketch = sketches.add(xyPlane)  

            #### Parameters (mm to cm) ####
            pin_radius = self.pin_radius
            pin_circle_radius = self.pitch_radius
            number_of_pins = self.number_of_pins
            contraction = self.contraction

            # the circumference of the rolling circle needs to be exactly equal to the pitch of the pins
            # rolling circle circumference = circumference of pin circle / number of pins
            rolling_circle_radius = pin_circle_radius / number_of_pins 
            reduction_ratio = number_of_pins + (1 if isInverse else -1) # reduction ratio
            cycloid_base_radius = reduction_ratio * rolling_circle_radius # base circle diameter of cycloidal disk
            eccentricity = rolling_circle_radius - contraction

            points = []
            lines = []

            # Calculate points- Only 190/360 degrees necessary, since it is trimmed later anyway.
            for angle in drange(0, 190/reduction_ratio, 0.2):
                if not isInverse:
                    points.append(calc_points_cycloid(angle, cycloid_base_radius, rolling_circle_radius, number_of_pins, contraction))
                else:
                    points.append(calc_points_inverse_cycloid(angle, cycloid_base_radius, rolling_circle_radius, number_of_pins, contraction))
                
            # Draw lines
            for c_i in range(len(points)):           
                p = points[c_i]
                if c_i == 0:
                    last_point = adsk.core.Point3D.create(p[0],p[1], 0)
                else:
                    line = sketch.sketchCurves.sketchLines.addByTwoPoints(
                            last_point, 
                            adsk.core.Point3D.create(p[0],p[1], 0)
                        )
                    last_point=line.endSketchPoint
                    lines.append(line)
            curves = sketch.findConnectedCurves(lines[0])

            # Create the offset.
            dirPoint = adsk.core.Point3D.create(0, 0, 0)
            offsetCurves = sketch.offset(curves, dirPoint, pin_radius * (-1 if isInverse else 1))
            offsetPoints = []

            # Get the points from the offset curves.
            for curve in offsetCurves:
                startPoint = curve.startSketchPoint.geometry
                endPoint = curve.endSketchPoint.geometry

                x1, y1, _ = startPoint.x, startPoint.y, startPoint.z
                x2, y2, _ = endPoint.x, endPoint.y, endPoint.z

                offsetPoints.append((x1, y1))
                offsetPoints.append((x2, y2))

            # Interpolate across the offset to reduce/optimise geometry
            int_points = interpolate_curve(offsetPoints, self.complexity)
            lines = []

            # Add missing line at x axis if isInverse. Missing because previous offset did not extend to X axis.
            if isInverse:
                int_points = [ [curves[0].startSketchPoint.geometry.x + pin_radius, 0] ] + int_points

            # Draw interpolated lines.
            for p_i in range(len(int_points)):           
                p = int_points[p_i]
                if p_i == 0:
                    last_point = adsk.core.Point3D.create(p[0],p[1], 0)
                else:
                    line = sketch.sketchCurves.sketchLines.addByTwoPoints(
                            last_point, 
                            adsk.core.Point3D.create(p[0],p[1], 0)
                        )
                    last_point=line.endSketchPoint
                    lines.append(line)

            # delete the originals
            self.design.deleteEntities(curves)
            self.design.deleteEntities(offsetCurves)

            # Calculate the end point coordinates for mirror line
            mirror_angle = (360 / reduction_ratio / 2 )
            mirror_end_x =  (pin_circle_radius + pin_radius) * cos(mirror_angle)
            mirror_end_y =  (pin_circle_radius + pin_radius) * sin(mirror_angle)
            
            # Create mirror line
            sketch_lines = sketch.sketchCurves.sketchLines
            mirror_line = sketch_lines.addByTwoPoints(
                adsk.core.Point3D.create(0, 0, 0), 
                adsk.core.Point3D.create(mirror_end_x, mirror_end_y, 0)
            )

            # Find where curve intersects mirror line.
            (returnValue, intersectingCurves, intersectionPoints)  = mirror_line.intersections(None)
            if returnValue:
                # If there is an intersecting line, trim it above the mirror line.
                intersectionPoints[0].x -= 0.00001
                intersectionPoints[0].y += 0.00001
                intersectingCurves[0].trim(intersectionPoints[0])

            # Delete the now redundant lines.
            vestigial_curves = sketch.findConnectedCurves(lines[-1])
            for curve in vestigial_curves:
                curve.deleteMe()

            # Take only the required lines, convert to points, mirror those points about the mirror line.
            curves_to_mirror = sketch.findConnectedCurves(lines[0])
            lines_coords = lines_to_points(curves_to_mirror)
            mirrored_lines_coords = mirror_points(lines_coords, mirror_end=[mirror_end_x, mirror_end_y])
            
            # Draw the new mirrored lines.
            mirrored_lines = []
            for c_i in range(len(mirrored_lines_coords)):           
                p = mirrored_lines_coords[c_i]
                if c_i == 0:
                    last_point = adsk.core.Point3D.create(p[0][0], p[0][1], 0)
                else:
                    line = sketch.sketchCurves.sketchLines.addByTwoPoints(
                            last_point, 
                            adsk.core.Point3D.create(p[1][0], p[1][1], 0)
                        )
                    last_point=line.endSketchPoint
                    mirrored_lines.append(line)

            mirror_line.deleteMe()  # No longer needed

            # Circular Pattern (Achieved through rotation copy)
            rotation_matrix = adsk.core.Matrix3D.create()
            step = 2 * math.pi / reduction_ratio

            # Copy lines from above and below the mirror line, around the origin, to form a complete cycloid.
            curves_original = sketch.findConnectedCurves(lines[0])
            curves_mirrored = sketch.findConnectedCurves(mirrored_lines[0])
            for i in range(1, reduction_ratio):
                rotation_matrix.setToRotation(step * i, adsk.core.Vector3D.create(0, 0, 1), adsk.core.Point3D.create(0, 0, 0))
                sketch.copy(curves_original, rotation_matrix)
                sketch.copy(curves_mirrored, rotation_matrix)

            # Add the pin circle sketch if requested
            if drawPin:
                sketch2 = sketches.add(xyPlane)  
                sketch2.sketchCurves.sketchCircles.addByCenterRadius(adsk.core.Point3D.create(pin_circle_radius + eccentricity, 0, 0), pin_radius)
                # add the pin Centre of Rotation
                sketch2.sketchPoints.add(adsk.core.Point3D.create(pin_circle_radius,0,0))

            self.app.activeViewport.refresh()

            self.ui.messageBox(f"Your eccentricity is: {int(eccentricity*10)}mm", "Cycloid Generated")

        except Exception as e:
            if self.ui:
                self.ui.messageBox("err "+str(e))

def stop(context):
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        
        # Delete the command definition.
        cmdDef = ui.commandDefinitions.itemById('GenerateCycloidId')
        if cmdDef:
            cmdDef.deleteMe()            
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
