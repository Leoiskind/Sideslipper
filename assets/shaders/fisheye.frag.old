#version 130

uniform sampler2D tex;
uniform float strength;   // 0 = no distortion, 1 = full distortion

in vec2 texcoord;
out vec4 fragColor;

void main() {
    vec2 uv = texcoord * 2.0 - 1.0;
    float r = length(uv);

    float k = 0.45;

    // distorted UV
    float f = 1.0 / (1.0 + k * r * r);
    vec2 warped = uv * f;

    // interpolate between original and distorted
    vec2 final_uv = mix(uv, warped, strength);

    final_uv = final_uv * 0.5 + 0.5;

    if (final_uv.x < 0.0 || final_uv.x > 1.0 || final_uv.y < 0.0 || final_uv.y > 1.0) {
        fragColor = vec4(0.0, 0.0, 0.0, 1.0);
        return;
    }

    fragColor = texture(tex, final_uv);
}