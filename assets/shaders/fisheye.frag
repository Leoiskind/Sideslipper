#version 130

uniform sampler2D tex;
uniform float strength;
uniform float pixel_size;

in vec2 texcoord;
out vec4 fragColor;

void main() {
    vec2 uv = texcoord * 2.0 - 1.0;
    float r = length(uv);

    float k = 0.45;

    // --- radial distortion ---
    float f = 1.0 / (1.0 + k * r * r);
    vec2 warped = uv * f;
    vec2 final_uv = mix(uv, warped, strength);
    final_uv = final_uv * 0.5 + 0.5;

    if (final_uv.x < 0.0 || final_uv.x > 1.0 || final_uv.y < 0.0 || final_uv.y > 1.0) {
        fragColor = vec4(0.0, 0.0, 0.0, 1.0);
        return;
    }

    // --- pixelation ---
    vec2 pixel_uv = floor(final_uv * pixel_size) / pixel_size;

    // --- chromatic aberration (static) ---
    float ca = 0.0001;

    float r_col = texture(tex, pixel_uv + vec2(ca, 0.0)).r;
    float g_col = texture(tex, pixel_uv).g;
    float b_col = texture(tex, pixel_uv - vec2(ca, 0.0)).b;

    vec3 col = vec3(r_col, g_col, b_col);

    // --- scanlines (static) ---
    float scan = sin(pixel_uv.y * 900.0) * 0.05;
    col -= scan;

    // --- vertical RGB mask (CRT subpixels) ---
    float mask = sin(pixel_uv.x * 1400.0);
    col.r *= 0.97 + 0.03 * mask;
    col.g *= 0.99;
    col.b *= 0.97 - 0.03 * mask;

    // --- vignette ---
	float vignette = 1.0 - r * 0.7;
	vignette = clamp(vignette, 0.6, 1.0);
	col *= vignette;

    fragColor = vec4(col, 0.5);
}