# Conditional Inference

Add Value as variable as 'var'

## Harsh Acceleration

route: /acc/

default: 11

condition : acceleration<11 && acceleration>-11

msg : "Harsh Acceleration/Retardation"

## Overspeeding

route: /speed/

default: 110

condition : speed>110

msg : "Speed over limit"

## Vehicle Engine

route: /engine/vehicle/

condition : ve>1.3 && ve<0.9

msg: "Reduce and "

## Engine Load

route: /engine/load/

condition : el<20 && 50>el

msg: "Engine load inappropriate."

map: "mechanic"

## Stopping

route: /stopping/

condition : time>12

msg: "Please turn off your engine."

# Boolean Inferences

## Coolant

msg: "Engine Coolant Circuit Error."

map: "mechanic"

## Engine MisFire

msg: "Engine might have an issue."

map: "mechanic"

## O2 Circuit Error

msg: "Error with O2 circuit"

map: "mechanic"