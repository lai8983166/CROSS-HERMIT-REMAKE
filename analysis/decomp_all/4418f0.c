
void __thiscall
FUN__text__004418f0(int param_1,char *param_2,int param_3,short param_4,short param_5,
                   undefined2 param_6)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_5c [16];
  int local_1c;
  int local_18;
  short local_14;
  short local_10;
  short local_c;
  int local_8;
  
  puVar3 = local_5c;
  for (iVar2 = 0x16; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_18 = (int)*param_2;
  local_1c = param_3;
  local_8 = param_1;
  if ((-1 < param_3) && (param_3 < 3)) {
    local_c = param_4;
    local_10 = param_5 + 0x84;
    FUN__text__00441ab0(param_1 + 4,2,CONCAT22((char)(&DAT_005ffc60)[param_3] >> 7,param_4),local_10
                        ,CONCAT22((short)((uint)(&DAT_005ffc38 + param_3 * 8) >> 0x10),param_6),
                        (int)(char)(&DAT_005ffc60)[param_3],&DAT_005ffc38 + param_3 * 8);
  }
  for (local_14 = 0; (int)local_14 != (int)param_2[1]; local_14 = local_14 + 1) {
    local_c = param_4 + 0x18;
    local_10 = param_5 + 0x18 + local_14 * 0x12;
    uVar1 = *(undefined4 *)(*(int *)(param_2 + 4) + local_14 * 4);
    FUN__text__00409810(CONCAT22((short)((uint)uVar1 >> 0x10),local_c),
                        CONCAT22((short)((uint)*(int *)(param_2 + 4) >> 0x10),local_10),0x12,0x16c,
                        param_6,0xffffffff,uVar1);
  }
  FUN__text__00441ab0(local_8 + 4,2,CONCAT22((char)(&DAT_005ffc64)[local_18] >> 7,param_4),param_5,
                      CONCAT22((short)((uint)(&DAT_005ffc50 + local_18 * 8) >> 0x10),param_6),
                      (int)(char)(&DAT_005ffc64)[local_18],&DAT_005ffc50 + local_18 * 8);
  local_8 = 0x441a3b;
  FUN__text__0056ce80();
  return;
}

