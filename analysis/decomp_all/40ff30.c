
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __thiscall FUN__text__0040ff30(int param_1,int param_2,uint param_3)

{
  int iVar1;
  float *pfVar2;
  undefined4 *puVar3;
  float *pfVar4;
  undefined4 local_e0 [16];
  int local_a0;
  int local_9c;
  int local_98;
  int local_94;
  int local_90;
  int local_8c;
  int local_88;
  int local_84;
  uint local_80;
  char local_7c;
  int local_78;
  float local_74;
  float local_70 [5];
  float local_5c;
  float local_58;
  undefined4 uStack_54;
  float local_48;
  float local_44;
  float local_34;
  float local_30;
  float local_20 [5];
  int local_c;
  int local_8;
  
  puVar3 = local_e0;
  for (iVar1 = 0x37; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = param_2;
  local_8 = param_1;
  (**(code **)(**(int **)(param_1 + 4) + 200))(*(undefined4 *)(param_1 + 4),0xf,1);
  FUN__text__0056ce80();
  (**(code **)(**(int **)(local_8 + 4) + 200))(*(undefined4 *)(local_8 + 4),0x18,8);
  FUN__text__0056ce80();
  (**(code **)(**(int **)(local_8 + 4) + 200))(*(undefined4 *)(local_8 + 4),0x19,5);
  FUN__text__0056ce80();
  local_7c = *(char *)(local_c + 8);
  if (local_7c == '\x01') {
    if ((*(uint *)(local_c + 0xc) & 0xff000000) != 0xff000000) {
      (**(code **)(**(int **)(local_8 + 4) + 200))(*(undefined4 *)(local_8 + 4),0x1b,1);
      FUN__text__0056ce80();
      (**(code **)(**(int **)(local_8 + 4) + 200))(*(undefined4 *)(local_8 + 4),0x13,5);
      FUN__text__0056ce80();
      (**(code **)(**(int **)(local_8 + 4) + 200))(*(undefined4 *)(local_8 + 4),0x14,6);
      FUN__text__0056ce80();
      goto LAB__text__004100e3;
    }
  }
  else if (local_7c == '\x02') {
    (**(code **)(**(int **)(local_8 + 4) + 200))(*(undefined4 *)(local_8 + 4),0x1b,1);
    FUN__text__0056ce80();
    (**(code **)(**(int **)(local_8 + 4) + 200))(*(undefined4 *)(local_8 + 4),0x13,5);
    FUN__text__0056ce80();
    (**(code **)(**(int **)(local_8 + 4) + 200))(*(undefined4 *)(local_8 + 4),0x14,7);
    FUN__text__0056ce80();
    goto LAB__text__004100e3;
  }
  (**(code **)(**(int **)(local_8 + 4) + 200))(*(undefined4 *)(local_8 + 4),0x1b,0);
  FUN__text__0056ce80();
LAB__text__004100e3:
  FUN__text__0040e210(0);
  (**(code **)(**(int **)(local_8 + 4) + 0x130))(*(undefined4 *)(local_8 + 4),0x44);
  FUN__text__0056ce80();
  local_80 = param_3 & 0xffff;
  local_74 = (float)local_80 / _DAT_00592774;
  for (local_78 = 0; local_78 != 4; local_78 = local_78 + 1) {
    local_70[local_78 * 5 + 2] = local_74;
    local_70[local_78 * 5 + 3] = 1.0;
    local_70[local_78 * 5 + 4] = *(float *)(local_c + 0xc);
  }
  local_84 = (int)*(short *)(local_c + 0x10);
  local_70[0] = (float)local_84;
  local_88 = (int)*(short *)(local_c + 0x12);
  local_70[1] = (float)local_88;
  local_8c = (int)*(short *)(local_c + 0x14);
  local_5c = (float)local_8c;
  local_90 = (int)*(short *)(local_c + 0x12);
  local_58 = (float)local_90;
  local_94 = (int)*(short *)(local_c + 0x14);
  local_48 = (float)local_94;
  local_98 = (int)*(short *)(local_c + 0x16);
  local_44 = (float)local_98;
  local_9c = (int)*(short *)(local_c + 0x10);
  local_34 = (float)local_9c;
  local_a0 = (int)*(short *)(local_c + 0x16);
  local_30 = (float)local_a0;
  pfVar2 = local_70;
  pfVar4 = local_20;
  for (iVar1 = 5; iVar1 != 0; iVar1 = iVar1 + -1) {
    *pfVar4 = *pfVar2;
    pfVar2 = pfVar2 + 1;
    pfVar4 = pfVar4 + 1;
  }
  (**(code **)(**(int **)(local_8 + 4) + 0x120))(*(undefined4 *)(local_8 + 4),3,4,local_70,0x14);
  FUN__text__0056ce80();
  uStack_54 = 0x41025b;
  FUN__text__0056ce80();
  return;
}

