
void __thiscall
FUN__text__00455d40(int param_1,int param_2,int param_3,undefined1 param_4,undefined1 param_5,
                   undefined1 param_6,undefined2 param_7,undefined1 param_8,undefined1 param_9,
                   undefined1 param_10)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_4c [16];
  undefined1 *local_c;
  int local_8;
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = param_1;
  if (param_2 < 0) {
    iVar2 = FUN__text__00424f80("0 <= timer","E:\\CrossHermit\\GAME\\src\\yoshida\\TacticsTask.cpp",
                                DAT_0060cda8 + 3,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_c = (undefined1 *)(*(int *)(local_8 + 0x60) + 0x2234 + param_3 * 0x10);
  if (param_2 == 0) {
    FUN__text__00455cb0(local_c);
  }
  else {
    *local_c = 1;
    *(int *)(local_c + 0xc) = param_2;
    local_c[1] = param_4;
    local_c[2] = param_5;
    local_c[3] = param_6;
    *(undefined2 *)(local_c + 4) = param_7;
    local_c[6] = param_8;
    local_c[7] = param_9;
    local_c[8] = param_10;
  }
  local_8 = 0x455e0e;
  FUN__text__0056ce80();
  return;
}

