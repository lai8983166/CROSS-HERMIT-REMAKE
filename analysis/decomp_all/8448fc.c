
uint FUN__text1__008448fc(uint param_1,int param_2)

{
  uint uVar1;
  uint uVar2;
  undefined4 local_8;
  
  local_8 = 0;
  uVar1 = local_8;
  do {
    local_8 = uVar1;
    uVar2 = param_1 & 1;
    param_1 = param_1 >> 1;
    param_2 = param_2 + -1;
    uVar1 = (local_8 | uVar2) << 1;
  } while (0 < param_2);
  return local_8 & 0x7fffffff | uVar2;
}

