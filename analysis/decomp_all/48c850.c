
void FUN__text__0048c850(int param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4,
                        int param_5,int param_6,undefined4 param_7,int param_8)

{
  byte bVar1;
  undefined4 uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_4c [16];
  undefined *local_c;
  undefined4 local_8;
  
  puVar4 = local_4c;
  for (iVar3 = 0x12; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  local_c = &DAT_006c2dc8 + param_1 * 0x48;
  FUN__text__0048b6c0(param_1,&local_c);
  uVar2 = FUN__text__004dfba0(*(undefined2 *)(*(int *)(param_6 + 600) + 0xc),param_2);
  *(undefined4 *)(param_8 + 0x20) = uVar2;
  iVar3 = FUN__text__004828a0(param_7,param_8,param_2,param_4);
  if ((iVar3 == 0) ||
     ((iVar3 = FUN__text__0046c9f0(param_1), iVar3 != 0 &&
      (bVar1 = *(byte *)(*(int *)(param_5 + 600) + 0x41),
      iVar3 = FUN__text__00467e00("E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAttack.cpp",
                                  DAT_00618f7c + 0xf), (int)(uint)bVar1 <= iVar3 % 100)))) {
    FUN__text__00495130(param_6,0);
  }
  else {
    FUN__text__00490180(param_6,param_3,param_2,param_4);
  }
  local_8 = 0x48c948;
  FUN__text__0056ce80();
  return;
}

