'use client';

import { useRef, useMemo, useEffect, useState } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import * as THREE from 'three';

interface NodeData {
  position: [number, number, number];
  id: string;
  size: number;
}

// Generate deterministic random positions using a seed
function seededRandom(seed: number): number {
  const x = Math.sin(seed) * 10000;
  return x - Math.floor(x);
}

function generateNodes(count: number): NodeData[] {
  const nodes: NodeData[] = [];
  for (let i = 0; i < count; i++) {
    const seed = i * 12345;
    // Vary node sizes for visual interest
    const sizeVariation = seededRandom(seed + 3);
    nodes.push({
      position: [
        (seededRandom(seed) - 0.5) * 14,
        (seededRandom(seed + 1) - 0.5) * 10,
        (seededRandom(seed + 2) - 0.5) * 8,
      ],
      id: `node-${i}`,
      size: 0.03 + sizeVariation * 0.08, // Size between 0.04 and 0.12
    });
  }
  return nodes;
}

function calculateEdges(nodes: NodeData[], maxDistance: number): [number, number][] {
  const edges: [number, number][] = [];
  for (let i = 0; i < nodes.length; i++) {
    for (let j = i + 1; j < nodes.length; j++) {
      const [x1, y1, z1] = nodes[i].position;
      const [x2, y2, z2] = nodes[j].position;
      const dist = Math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2);
      if (dist < maxDistance) {
        edges.push([i, j]);
      }
    }
  }
  return edges;
}

function NetworkScene() {
  const groupRef = useRef<THREE.Group>(null);
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });
  const [prefersReducedMotion, setPrefersReducedMotion] = useState(false);

  // Check for reduced motion preference
  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
    setPrefersReducedMotion(mediaQuery.matches);
    const handler = (e: MediaQueryListEvent) => setPrefersReducedMotion(e.matches);
    mediaQuery.addEventListener('change', handler);
    return () => mediaQuery.removeEventListener('change', handler);
  }, []);

  // Track mouse position for parallax
  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      // Normalize to -1 to 1
      const x = (e.clientX / window.innerWidth) * 2 - 1;
      const y = -(e.clientY / window.innerHeight) * 2 + 1;
      setMousePosition({ x, y });
    };
    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);

  // Generate nodes and edges - many more nodes for visual impact
  const nodes = useMemo(() => generateNodes(150), []);
  const edges = useMemo(() => calculateEdges(nodes, 2.5), [nodes]);

  // Create edge geometry
  const edgeGeometry = useMemo(() => {
    const positions: number[] = [];
    edges.forEach(([i, j]) => {
      positions.push(...nodes[i].position, ...nodes[j].position);
    });
    const geometry = new THREE.BufferGeometry();
    geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
    return geometry;
  }, [nodes, edges]);

  // Animation frame
  useFrame((_state, delta) => {
    if (!groupRef.current || prefersReducedMotion) return;

    // Slow auto-rotation
    groupRef.current.rotation.y += delta * 0.08;

    // Subtle parallax based on mouse position
    const targetRotationX = mousePosition.y * 0.15;
    const targetRotationZ = mousePosition.x * 0.1;

    groupRef.current.rotation.x += (targetRotationX - groupRef.current.rotation.x) * 0.05;
    groupRef.current.rotation.z += (targetRotationZ - groupRef.current.rotation.z) * 0.05;
  });

  return (
    <group ref={groupRef}>
      {/* Nodes as small spheres with varying sizes */}
      {nodes.map((node) => (
        <mesh key={node.id} position={node.position}>
          <sphereGeometry args={[node.size, 12, 12]} />
          <meshStandardMaterial
            color="#ffffff"
            emissive="#7dd3fc"
            emissiveIntensity={1.2}
            roughness={0.2}
            metalness={0.2}
          />
        </mesh>
      ))}

      {/* Edges as lines */}
      <lineSegments geometry={edgeGeometry}>
        <lineBasicMaterial color="#7dd3fc" transparent opacity={1} />
      </lineSegments>

      {/* Ambient glow particles */}
      {[0, 1, 2].map((i) => (
        <pointLight
          key={`light-${i}`}
          position={[
            Math.cos((i / 3) * Math.PI * 2) * 4,
            Math.sin((i / 3) * Math.PI * 2) * 4,
            2,
          ]}
          intensity={1.4}
          color="#38bdf8"
          distance={12}
        />
      ))}
    </group>
  );
}

interface NetworkGraph3DProps {
  className?: string;
}

export function NetworkGraph3D({ className }: NetworkGraph3DProps) {
  return (
    <div className={`w-full h-full ${className || ''}`}>
      <Canvas
        camera={{ position: [0, 0, 12], fov: 60 }}
        style={{ background: 'transparent' }}
        gl={{ antialias: true, alpha: true }}
      >
        {/* Ambient lighting for overall visibility */}
        <ambientLight intensity={1} />

        {/* Main directional light from top */}
        <directionalLight position={[5, 8, 5]} intensity={0.8} color="#ffffff" />

        {/* Secondary light from front-top */}
        <directionalLight position={[0, 6, 8]} intensity={0.5} color="#e0f2fe" />

        {/* Accent light from behind */}
        <directionalLight position={[-3, -3, -5]} intensity={0.4} color="#38bdf8" />

        <NetworkScene />
      </Canvas>
    </div>
  );
}

export default NetworkGraph3D;
