
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __thiscall FUN__text__0040edd0(int param_1,int param_2,uint param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_c8 [16];
  char local_88;
  int local_84;
  int local_80;
  int local_7c;
  int local_78;
  int local_74;
  int local_70;
  uint local_6c;
  int local_68;
  int local_64;
  float local_60;
  float local_5c;
  float local_58;
  undefined4 local_54;
  undefined4 local_50;
  float local_4c;
  float local_48;
  float local_44;
  undefined4 local_40;
  undefined4 local_3c;
  float local_38;
  float local_34;
  float local_30;
  undefined4 local_2c;
  undefined4 local_28;
  float local_24;
  float local_20;
  float local_1c;
  undefined4 local_18;
  undefined4 local_14;
  int local_10;
  undefined4 local_c;
  int local_8;
  
  puVar2 = local_c8;
  for (iVar1 = 0x31; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_10 = param_2;
  local_64 = (int)*(short *)(param_2 + 10);
  local_60 = (float)local_64;
  local_68 = (int)*(short *)(param_2 + 0xc);
  local_5c = (float)local_68;
  local_6c = param_3 & 0xffff;
  local_58 = (float)local_6c / _DAT_00592774;
  local_54 = 0x3f800000;
  local_50 = *(undefined4 *)(param_2 + 0x14);
  local_70 = (int)*(short *)(param_2 + 10) + (int)*(short *)(param_2 + 0xe);
  local_4c = (float)local_70;
  local_74 = (int)*(short *)(param_2 + 0xc);
  local_48 = (float)local_74;
  local_40 = 0x3f800000;
  local_3c = *(undefined4 *)(param_2 + 0x14);
  local_78 = (int)*(short *)(param_2 + 10) + (int)*(short *)(param_2 + 0xe);
  local_38 = (float)local_78;
  local_7c = (int)*(short *)(param_2 + 0xc) + (int)*(short *)(param_2 + 0x10);
  local_34 = (float)local_7c;
  local_2c = 0x3f800000;
  local_28 = *(undefined4 *)(param_2 + 0x14);
  local_80 = (int)*(short *)(param_2 + 10);
  local_24 = (float)local_80;
  local_84 = (int)*(short *)(param_2 + 0xc) + (int)*(short *)(param_2 + 0x10);
  local_20 = (float)local_84;
  local_18 = 0x3f800000;
  local_14 = *(undefined4 *)(param_2 + 0x14);
  local_44 = local_58;
  local_30 = local_58;
  local_1c = local_58;
  local_8 = param_1;
  (**(code **)(**(int **)(param_1 + 4) + 200))(*(undefined4 *)(param_1 + 4),0xf,0);
  FUN__text__0056ce80();
  local_88 = *(char *)(local_10 + 8);
  if (local_88 == '\x01') {
    if ((*(uint *)(local_10 + 0x14) & 0xff000000) != 0xff000000) {
      (**(code **)(**(int **)(local_8 + 4) + 200))(*(undefined4 *)(local_8 + 4),0x1b,1);
      FUN__text__0056ce80();
      (**(code **)(**(int **)(local_8 + 4) + 200))(*(undefined4 *)(local_8 + 4),0x13,5);
      FUN__text__0056ce80();
      (**(code **)(**(int **)(local_8 + 4) + 200))(*(undefined4 *)(local_8 + 4),0x14,6);
      FUN__text__0056ce80();
      goto LAB__text__0040f056;
    }
  }
  else if (local_88 == '\x02') {
    (**(code **)(**(int **)(local_8 + 4) + 200))(*(undefined4 *)(local_8 + 4),0x1b,1);
    FUN__text__0056ce80();
    (**(code **)(**(int **)(local_8 + 4) + 200))(*(undefined4 *)(local_8 + 4),0x13,5);
    FUN__text__0056ce80();
    (**(code **)(**(int **)(local_8 + 4) + 200))(*(undefined4 *)(local_8 + 4),0x14,7);
    FUN__text__0056ce80();
    goto LAB__text__0040f056;
  }
  (**(code **)(**(int **)(local_8 + 4) + 200))(*(undefined4 *)(local_8 + 4),0x1b,0);
  FUN__text__0056ce80();
LAB__text__0040f056:
  FUN__text__0040e210(0);
  (**(code **)(**(int **)(local_8 + 4) + 0x130))(*(undefined4 *)(local_8 + 4),0x44);
  FUN__text__0056ce80();
  (**(code **)(**(int **)(local_8 + 4) + 0x120))(*(undefined4 *)(local_8 + 4),6,2,&local_60,0x14);
  local_c = FUN__text__0056ce80();
  local_3c = 0x40f0bd;
  FUN__text__0056ce80();
  return;
}

