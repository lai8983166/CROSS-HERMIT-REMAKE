
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __thiscall FUN__text__0040e650(int param_1,int param_2,uint param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_f0 [16];
  char local_b0;
  uint local_ac;
  undefined4 local_a8;
  uint local_a4;
  uint local_a0;
  uint local_9c;
  uint local_98;
  uint local_94;
  int local_90;
  undefined4 local_8c;
  undefined4 local_88;
  float local_84;
  undefined4 local_80;
  uint local_7c;
  uint local_78;
  undefined4 local_74;
  undefined4 local_70;
  undefined4 local_6c;
  undefined4 local_68;
  float local_64;
  undefined4 local_60;
  uint local_5c;
  uint local_58;
  undefined4 local_54;
  undefined4 local_50;
  undefined4 local_4c;
  undefined4 local_48;
  float local_44;
  undefined4 local_40;
  uint local_3c;
  uint local_38;
  undefined4 local_34;
  undefined4 local_30;
  undefined4 local_2c;
  undefined4 local_28;
  float local_24;
  undefined4 local_20;
  uint local_1c;
  uint local_18;
  undefined4 local_14;
  undefined4 local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_f0;
  for (iVar1 = 0x3b; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = param_2;
  local_9c = (*(uint *)(param_2 + 0x4c) & 0xff0000) >> 0x10;
  local_a0 = (*(uint *)(param_2 + 0x4c) & 0xff00) >> 8;
  local_a4 = *(uint *)(param_2 + 0x4c) & 0xff;
  local_94 = *(uint *)(param_2 + 0x4c) & 0xff000000 | (uint)(byte)(&DAT_005ff148)[local_9c] << 0x10
             | (uint)(byte)(&DAT_005ff148)[local_a0] << 8 | (uint)(byte)(&DAT_005ff148)[local_a4];
  local_98 = (uint)(byte)(&DAT_005ff248)[local_9c] << 0x10 |
             (uint)(byte)(&DAT_005ff248)[local_a0] << 8 | (uint)(byte)(&DAT_005ff248)[local_a4];
  local_8c = *(undefined4 *)(param_2 + 0xc);
  local_88 = *(undefined4 *)(param_2 + 0x1c);
  local_ac = param_3 & 0xffff;
  local_84 = (float)local_ac / _DAT_00592774;
  local_80 = 0x3f800000;
  local_74 = *(undefined4 *)(param_2 + 0x2c);
  local_70 = *(undefined4 *)(param_2 + 0x3c);
  local_6c = *(undefined4 *)(param_2 + 0x10);
  local_68 = *(undefined4 *)(param_2 + 0x20);
  local_60 = 0x3f800000;
  local_54 = *(undefined4 *)(param_2 + 0x30);
  local_50 = *(undefined4 *)(param_2 + 0x40);
  local_4c = *(undefined4 *)(param_2 + 0x14);
  local_48 = *(undefined4 *)(param_2 + 0x24);
  local_40 = 0x3f800000;
  local_34 = *(undefined4 *)(param_2 + 0x34);
  local_30 = *(undefined4 *)(param_2 + 0x44);
  local_2c = *(undefined4 *)(param_2 + 0x18);
  local_28 = *(undefined4 *)(param_2 + 0x28);
  local_20 = 0x3f800000;
  local_14 = *(undefined4 *)(param_2 + 0x38);
  local_10 = *(undefined4 *)(param_2 + 0x48);
  local_7c = local_94;
  local_78 = local_98;
  local_64 = local_84;
  local_5c = local_94;
  local_58 = local_98;
  local_44 = local_84;
  local_3c = local_94;
  local_38 = local_98;
  local_24 = local_84;
  local_1c = local_94;
  local_18 = local_98;
  local_8 = param_1;
  (**(code **)(**(int **)(param_1 + 4) + 200))(*(undefined4 *)(param_1 + 4),0xf,1);
  FUN__text__0056ce80();
  (**(code **)(**(int **)(local_8 + 4) + 200))(*(undefined4 *)(local_8 + 4),0x18,8);
  FUN__text__0056ce80();
  (**(code **)(**(int **)(local_8 + 4) + 200))(*(undefined4 *)(local_8 + 4),0x19,5);
  FUN__text__0056ce80();
  local_b0 = *(char *)(local_c + 9);
  if (local_b0 == '\x01') {
    if ((*(uint *)(local_c + 0x4c) & 0xff000000) != 0xff000000) {
      (**(code **)(**(int **)(local_8 + 4) + 200))(*(undefined4 *)(local_8 + 4),0x1b,1);
      FUN__text__0056ce80();
      (**(code **)(**(int **)(local_8 + 4) + 200))(*(undefined4 *)(local_8 + 4),0x13,5);
      FUN__text__0056ce80();
      (**(code **)(**(int **)(local_8 + 4) + 200))(*(undefined4 *)(local_8 + 4),0x14,6);
      FUN__text__0056ce80();
      goto LAB__text__0040e9f3;
    }
  }
  else if (local_b0 == '\x02') {
    (**(code **)(**(int **)(local_8 + 4) + 200))(*(undefined4 *)(local_8 + 4),0x1b,1);
    FUN__text__0056ce80();
    (**(code **)(**(int **)(local_8 + 4) + 200))(*(undefined4 *)(local_8 + 4),0x13,5);
    FUN__text__0056ce80();
    (**(code **)(**(int **)(local_8 + 4) + 200))(*(undefined4 *)(local_8 + 4),0x14,7);
    FUN__text__0056ce80();
    goto LAB__text__0040e9f3;
  }
  (**(code **)(**(int **)(local_8 + 4) + 200))(*(undefined4 *)(local_8 + 4),0x1b,0);
  FUN__text__0056ce80();
LAB__text__0040e9f3:
  local_90 = *(int *)(local_c + 0x50);
  FUN__text__0040e210(*(undefined4 *)(local_90 + 0x2c));
  (**(code **)(**(int **)(local_8 + 4) + 0x130))(*(undefined4 *)(local_8 + 4),0x1c4);
  FUN__text__0056ce80();
  (**(code **)(**(int **)(local_8 + 4) + 0x120))(*(undefined4 *)(local_8 + 4),6,2,&local_8c,0x20);
  local_a8 = FUN__text__0056ce80();
  local_54 = 0x40ea77;
  FUN__text__0056ce80();
  return;
}

