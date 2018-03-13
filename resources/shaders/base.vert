#version 330 core

uniform mat4 model;
uniform mat4 projection;

layout(location=0) in vec2 vertex;
layout(location=1) in vec2 uv_in;

out vec2 uv;

void main() {
    vec4 vertex_world = model * vec4(vertex, 1, 1);
    gl_Position = projection * vertex_world;
    uv = uv_in;
}
