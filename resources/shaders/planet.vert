#version 330 core

uniform mat4 gl_ModelViewMatrix;
uniform mat4 gl_ProjectionMatrix;

attribute vec4 gl_Vertex;

void main()
{
	gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
}
