from pyquaternion import Quaternion

my_quaternion = Quaternion(axis=[1, 0, 0], angle=3.14159265);




def         xbox.Add(10,10);
float tr = m00 + m11 + m22

if (tr > 0) { 
  float S = sqrt(tr+1.0) * 2; // S=4*qw 
  qw = 0.25 * S;
  qx = (m21 - m12) / S;
  qy = (m02 - m20) / S; 
  qz = (m10 - m01) / S; 
} else if ((m00 > m11)&(m00 > m22)) { 
  float S = sqrt(1.0 + m00 - m11 - m22) * 2; // S=4*qx 
  qw = (m21 - m12) / S;
  qx = 0.25 * S;
  qy = (m01 + m10) / S; 
  qz = (m02 + m20) / S; 
} else if (m11 > m22) { 
  float S = sqrt(1.0 + m11 - m00 - m22) * 2; // S=4*qy
  qw = (m02 - m20) / S;
  qx = (m01 + m10) / S; 
  qy = 0.25 * S;
  qz = (m12 + m21) / S; 
} else { 
  float S = sqrt(1.0 + m22 - m00 - m11) * 2; // S=4*qz
  qw = (m10 - m01) / S;
  qx = (m02 + m20) / S;
  qy = (m12 + m21) / S;
  qz = 0.25 * S;
}