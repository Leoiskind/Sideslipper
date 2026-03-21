#version 130

uniform sampler2D p3d_Texture0;
uniform float strength;
uniform float time;
uniform float pixel_size;

in vec2 uv;
out vec4 fragColor;

void main() {
    vec2 center = vec2(0.5, 0.5);

    // --------------------------------------------------
    // 1. PIXELATION (screen space — CRITICAL)
    // --------------------------------------------------
    vec2 pixel_uv = floor(uv * pixel_size) / pixel_size;

    // --------------------------------------------------
    // 2. DISTORTION (applied to pixel blocks)
    // --------------------------------------------------
    vec2 d = pixel_uv - center;
    float r = length(d);

    // --- CRT-style radial distortion ---
    float k = 0.45;
    float f = 1.0 / (1.0 + k * r * r);

    // blend with your original warp for control
    float warp = 1.0 + strength * 2.5 * r * r;
    vec2 warped = center + d / warp;

    vec2 crt_warped = center + d * f;

    // mix both distortions
    vec2 uv2 = mix(pixel_uv, warped, strength);
    uv2 = mix(uv2, crt_warped, 0.5 * strength);

    // --- wobble ---
    uv2.x += sin(pixel_uv.y * 22.0 + time * 4.0) * 0.1 * strength;
    uv2.y += cos(pixel_uv.x * 18.0 - time * 3.5) * 0.1 * strength;

    // --------------------------------------------------
    // 3. SCREEN BOUNDS (CRT cutoff)
    // --------------------------------------------------
    if (uv2.x < 0.0 || uv2.x > 1.0 || uv2.y < 0.0 || uv2.y > 1.0) {
        fragColor = vec4(0.0, 0.0, 0.0, 1.0);
        return;
    }

    // --------------------------------------------------
    // 4. CHROMATIC ABERRATION
    // --------------------------------------------------
    float ca = 0.006 * strength;

    float r_col = texture(p3d_Texture0, uv2 + vec2(ca, 0.0)).r;
    float g_col = texture(p3d_Texture0, uv2).g;
    float b_col = texture(p3d_Texture0, uv2 - vec2(ca, 0.0)).b;

    vec3 col = vec3(r_col, g_col, b_col);

    // --------------------------------------------------
    // 5. CRT EFFECTS (IMPORTANT: use pixel_uv, not uv2)
    // --------------------------------------------------

    // --- scanlines ---
    float scan = sin(pixel_uv.y * 900.0) * 0.05;
    col -= scan;

    // --- vertical RGB mask (subpixel effect) ---
    float mask = sin(pixel_uv.x * 1400.0);
    col.r *= 0.97 + 0.03 * mask;
    col.g *= 0.99;
    col.b *= 0.97 - 0.03 * mask;

    // --------------------------------------------------
    // 6. VIGNETTE (optional, CRT-style)
    // --------------------------------------------------
    //float vignette = 1.0 - length(uv - center) * 0.7;
    //vignette = clamp(vignette, 0.6, 1.0);
    //col *= vignette;

    fragColor = vec4(col, 1.0);
}