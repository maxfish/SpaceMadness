#version 330 core

in vec2 uv;
out vec4 color;
uniform sampler2D tex;

void main() {
    float distanceFromCenter = length( uv - vec2(0.5,0.5) );
    float vignetteAmount = 1 - distanceFromCenter;
    vignetteAmount = smoothstep(0.1, 1.0, vignetteAmount);

    vec4 c = texture(tex, uv);
    c *= 0.9 + 0.4*16.0*uv.x*uv.y*(1.0-uv.x)*(1.0-uv.y);
    c *= clamp(mod(uv.y*720, 2.0) + 0.3, 0, 1.0);
    c.a = 1.0;
    color = c;
}
