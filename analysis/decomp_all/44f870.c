
void __thiscall
FUN__text__0044f870(int param_1,undefined2 param_2,undefined2 param_3,ushort param_4,ushort param_5,
                   int param_6,undefined4 param_7,undefined4 param_8)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  int local_c;
  int local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  *(undefined4 *)(param_1 + 0xc) = param_7;
  local_8 = param_1;
  local_c = FUN__text__0044f680(param_2,param_3,param_4,param_5,param_8);
  if (local_c != 0) {
    FUN__text__0044e9a0(param_6);
    *(ushort *)(param_6 + 0x18) = param_4 & 0xff;
    *(ushort *)(param_6 + 0x1a) = param_5 & 0xff;
    *(undefined1 *)(param_6 + 0x1c) = (undefined1)param_2;
    *(undefined1 *)(param_6 + 0x1d) = (undefined1)param_3;
    *(undefined2 *)(param_6 + 0x1e) = 0;
    *(undefined2 *)(param_6 + 0x20) = 1;
    *(undefined1 *)(param_6 + 0x22) = (undefined1)param_4;
    *(undefined1 *)(param_6 + 0x23) = (undefined1)param_5;
  }
  local_8 = 0x44f92f;
  FUN__text__0056ce80();
  return;
}

