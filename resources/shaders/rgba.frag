#version 330 core

in vec2 uv;
out vec4 color;

uniform sampler2D tex;
uniform float mul_r;
uniform float mul_g;
uniform float mul_b;
uniform float mul_a;

void main() {
    color = texture(tex, uv);
    color.r *= 1 - mul_r;
    color.g *= 1 - mul_g;
    color.b *= 1 - mul_b;
    color.a *= 1 - mul_a;
}