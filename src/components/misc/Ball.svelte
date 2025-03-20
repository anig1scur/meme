<script>
  import {T, Canvas, extend} from '@threlte/core';
  import {onMount} from 'svelte';
  import {TextureLoader, Clock, DoubleSide} from 'three';
  import * as THREE from 'three';
  extend(THREE);

  const clock = new Clock();
  const rotationSpeed = 0.3;
  const textureLoader = new TextureLoader();

  let figures = Object.values(
    import.meta.glob(['$assets/imgs/intro/*.jpg', '$assets/imgs/intro/*.png'], {
      eager: true,
      as: 'url',
    }),
  );
  figures = figures.concat(figures);

  let materialsArray = [];
  let dodecahedronMesh;

  onMount(async () => {
    if (figures.length < 12) {
      console.error('at least 12 figures ');
      return;
    }

    const textures = await Promise.all(
      figures.slice(0, 12).map((url) => {
        return new Promise((resolve, reject) => {
          textureLoader.load(
            url,
            (texture) => {
              texture.flipY = false;
              texture.wrapS = THREE.ClampToEdgeWrapping;
              texture.wrapT = THREE.ClampToEdgeWrapping;
              resolve(texture);
            },
            undefined,
            reject,
          );
        });
      }),
    );

    materialsArray = textures.map(
      (texture) =>
        new THREE.MeshStandardMaterial({
          map: texture,
          side: DoubleSide,
          roughness: 0.5,
          metalness: 0.1,
        }),
    );

    const geometry = new THREE.DodecahedronGeometry(1, 0);

    const positionAttribute = geometry.attributes.position;
    let faceCount = positionAttribute.count / 3;

    let materialIndices = [];
    for (let i = 0; i < faceCount; i++) {
      materialIndices.push(i % 12, i % 12, i % 12);
    }

    geometry.setAttribute('materialIndex', new THREE.Float32BufferAttribute(materialIndices, 1));

    for (let i = 0; i < faceCount; i++) {
      geometry.addGroup(i * 3, 3, i % 12);
    }

    if (dodecahedronMesh) {
      dodecahedronMesh.geometry = geometry;
      dodecahedronMesh.material = materialsArray;
    }
  });

  let rotationX = 0;
  let rotationY = 0;

  function animate() {
    const delta = clock.getDelta();
    rotationY += delta * rotationSpeed;
    rotationX += delta * rotationSpeed * 0.2;
    requestAnimationFrame(animate);
  }

  onMount(() => {
    requestAnimationFrame(animate);
  });

  let ambientIntensity = 1.0;
  let directionalIntensity = 1.5;
</script>

<div class="fixed z-10 -top-8 left-4 w-16 h-16 opacity-0" id="ball">
  <Canvas>
    <T.PerspectiveCamera
      position={[0, 0, 5]}
      fov={60}
      near={0.1}
      far={1000}
    />

    <T.AmbientLight intensity={ambientIntensity} />

    <T.DirectionalLight
      position={[5, 5, 5]}
      intensity={directionalIntensity}
      castShadow
    />
    <T.DirectionalLight
      position={[-5, -5, -5]}
      intensity={directionalIntensity * 0.5}
    />

    <T.Group rotation={[rotationX, rotationY, 0]}>
      <T.Mesh
        receiveShadow
        castShadow
        bind:ref={dodecahedronMesh}
      >
        <T.DodecahedronGeometry args={[1, 0]} />
        <T
          is={THREE.MeshBasicMaterial}
          args={[{visible: false}]}
        />
      </T.Mesh>
    </T.Group>
  </Canvas>
</div>
