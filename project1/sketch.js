function setup() {
	createCanvas(windowWidth, windowHeight);
	// put setup code here
	frameRate(20)
}

t = 0 
PI = 3.1415
R = 200 
prevx = 200
prevy = 400
let r = R*4/PI 
let wave = [] 


async function draw() {
	// put drawing code here
	t +=.05
	background(0,255,150);
	prevx = 200
	prevy = 400
	noFill()
	circle(prevx,prevy,2*r)
	for (let index = 0; index < 100; index++) {
		n1 = 2*index + 1 
		n = 1/(n1)
		x = prevx + r*n*cos(n1*t)
		y = prevy + r*n*sin(n1*t)
		noFill()
		circle(x,y,r*n)
		fill(255,255,255)
		circle(x,y,10)
		line(prevx,prevy,x,y)
		prevx = x 
		prevy = y
	}
	noFill()
	wave.unshift(y)

	translate(500,0)
	line(x-500,y,0,wave[0])
	beginShape()
	for (let i = 0; i < wave.length; i++) {
		vertex(i,wave[i])
	}
	endShape()
	fill(155,255,0)
	circle(0,wave[0],20)
	
}

