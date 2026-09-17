
/* Library Function - Single Match
    ___shl_12
   
   Libraries: Visual Studio 2003, Visual Studio 2005, Visual Studio 2008, Visual Studio 2010 */

void ___shl_12(uint *param_1)

{
  uint uVar1;
  uint uVar2;
  
  uVar1 = *param_1;
  uVar2 = param_1[1];
  *param_1 = *param_1 << 1;
  param_1[1] = param_1[1] << 1 | (uint)((uVar1 & 0x80000000) != 0);
  param_1[2] = param_1[2] << 1 | (uint)((uVar2 & 0x80000000) != 0);
  return;
}

