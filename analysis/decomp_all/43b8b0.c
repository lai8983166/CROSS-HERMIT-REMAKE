
void __thiscall FUN__text__0043b8b0(int param_1,int param_2,int param_3,int param_4,int param_5)

{
  byte bVar1;
  code *pcVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_50 [16];
  byte local_10;
  undefined3 uStack_f;
  int local_c;
  int local_8;
  
  puVar4 = local_50;
  for (iVar3 = 0x13; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  if ((((-1 < param_2) && (-1 < param_3)) && (param_2 < *(short *)(*(int *)(param_1 + 0x2659c) + 4))
      ) && (param_3 < *(short *)(*(int *)(param_1 + 0x2659c) + 6))) {
    local_8 = param_1;
    if (((param_4 < 0) || (4 < param_4)) &&
       (iVar3 = FUN__text__00424f80("(0<=type)&&(type<=4)",
                                    "E:\\CrossHermit\\GAME\\src\\yoshida\\MapCtrl.cpp",
                                    DAT_005ff9e0 + 10,0), iVar3 != 0)) {
      pcVar2 = (code *)swi(3);
      (*pcVar2)();
      return;
    }
    if (param_4 == 4) {
      param_4 = 0;
    }
    bVar1 = *(byte *)(*(int *)(local_8 + 0x2659c) + 0x10 +
                     (param_3 * *(short *)(*(int *)(local_8 + 0x2659c) + 4) + param_2) * 6);
    _local_10 = CONCAT31(uStack_f,bVar1);
    local_c = *(int *)(*(int *)(local_8 + 0x8c) + (uint)bVar1 * 0x4c + 0xc + param_4 * 0x10 +
                      param_5 * 4);
    if (local_c == 0) {
      local_c = 0x32;
    }
  }
  local_8 = 0x43b9cb;
  FUN__text__0056ce80();
  return;
}

