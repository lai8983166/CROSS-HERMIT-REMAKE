
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __thiscall FUN__text__0040fc20(int param_1,int param_2,uint param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_134 [16];
  uint local_f4;
  int local_f0;
  int local_ec;
  uint local_e8;
  char local_e4;
  float local_e0;
  uint local_dc;
  uint local_d8;
  float local_d4 [38];
  undefined4 uStack_3c;
  int local_c;
  int local_8;
  
  puVar2 = local_134;
  for (iVar1 = 0x4c; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = param_2;
  local_8 = param_1;
  (**(code **)(**(int **)(param_1 + 4) + 200))(*(undefined4 *)(param_1 + 4),0xf,0);
  FUN__text__0056ce80();
  local_e4 = *(char *)(local_c + 8);
  if (local_e4 == '\x01') {
    if ((*(uint *)(local_c + 0xc) & 0xff000000) != 0xff000000) {
      (**(code **)(**(int **)(local_8 + 4) + 200))(*(undefined4 *)(local_8 + 4),0x1b,1);
      FUN__text__0056ce80();
      (**(code **)(**(int **)(local_8 + 4) + 200))(*(undefined4 *)(local_8 + 4),0x13,5);
      FUN__text__0056ce80();
      (**(code **)(**(int **)(local_8 + 4) + 200))(*(undefined4 *)(local_8 + 4),0x14,6);
      FUN__text__0056ce80();
      goto LAB__text__0040fd98;
    }
  }
  else if (local_e4 == '\x02') {
    (**(code **)(**(int **)(local_8 + 4) + 200))(*(undefined4 *)(local_8 + 4),0x1b,1);
    FUN__text__0056ce80();
    (**(code **)(**(int **)(local_8 + 4) + 200))(*(undefined4 *)(local_8 + 4),0x13,5);
    FUN__text__0056ce80();
    (**(code **)(**(int **)(local_8 + 4) + 200))(*(undefined4 *)(local_8 + 4),0x14,7);
    FUN__text__0056ce80();
    goto LAB__text__0040fd98;
  }
  (**(code **)(**(int **)(local_8 + 4) + 200))(*(undefined4 *)(local_8 + 4),0x1b,0);
  FUN__text__0056ce80();
LAB__text__0040fd98:
  FUN__text__0040e210(0);
  (**(code **)(**(int **)(local_8 + 4) + 0x130))(*(undefined4 *)(local_8 + 4),0x44);
  FUN__text__0056ce80();
  local_e8 = param_3 & 0xffff;
  local_e0 = (float)local_e8 / _DAT_00592774;
  if (*(byte *)(local_c + 9) < 0xb) {
    local_d8 = (uint)*(byte *)(local_c + 9);
  }
  else {
    local_d8 = 10;
  }
  for (local_dc = 0; local_dc != local_d8; local_dc = local_dc + 1) {
    local_ec = (int)*(short *)(local_c + 0x10 + local_dc * 4);
    local_d4[local_dc * 5] = (float)local_ec;
    local_f0 = (int)*(short *)(local_c + 0x12 + local_dc * 4);
    local_d4[local_dc * 5 + 1] = (float)local_f0;
    local_f4 = param_3 & 0xffff;
    local_d4[local_dc * 5 + 2] = (float)local_f4;
    local_d4[local_dc * 5 + 3] = 1.0;
    local_d4[local_dc * 5 + 4] = *(float *)(local_c + 0xc);
  }
  (**(code **)(**(int **)(local_8 + 4) + 0x120))
            (*(undefined4 *)(local_8 + 4),3,local_d8 - 1,local_d4,0x14);
  FUN__text__0056ce80();
  uStack_3c = 0x40ff24;
  FUN__text__0056ce80();
  return;
}

