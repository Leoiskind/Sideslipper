#version 130
uniform sampler2D p3d_Texture0;
uniform float strength;
uniform float time;

in vec2 uv;
out vec4 fragColor;

void main() {
    vec2 center = vec2(0.5, 0.5);
    vec2 d = uv - center;
    float r = length(d);

    // Stronger radial warp
    float warp = 1.0 + strength * 2.5 * r * r;
    vec2 uv2 = center + d / warp;

    // Stronger wobble: do NOT multiply the phase by strength
    uv2.x += sin(uv.y * 22.0 + time * 4.0) * 0.1 * strength;
    uv2.y += cos(uv.x * 18.0 - time * 3.5) * 0.1 * strength;

    // Stronger chromatic aberration
    float ca = 0.006 * strength;
    vec4 col;
    col.r = texture(p3d_Texture0, uv2 + vec2(ca, 0.0)).r;
    col.g = texture(p3d_Texture0, uv2).g;
    col.b = texture(p3d_Texture0, uv2 - vec2(ca, 0.0)).b;
    col.a = texture(p3d_Texture0, uv2).a;

    // Stronger vignette
    float vignette = smoothstep(1.0, 0.15, r);
    col.rgb *= vignette;

    fragColor = col;
}