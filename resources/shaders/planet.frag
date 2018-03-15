#version 330 core

in vec2 uv;
out vec4 color;

uniform sampler2D tex;

void main()
{
	gl_FragColor = vec4(0.4,0.4,0.8,1.0);
}
