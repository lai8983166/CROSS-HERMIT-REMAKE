
void __fastcall FUN__text__00481fc0(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [16];
  char local_10;
  char *local_c;
  int local_8;
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = (char *)(param_1 + 0x115cac);
  *(undefined2 *)(param_1 + 0x115cb4) = *(undefined2 *)(DAT_007a49fc + 0x196c);
  *(undefined2 *)(param_1 + 0x115cb6) = *(undefined2 *)(DAT_007a49fc + 0x1970);
  local_10 = *local_c;
  if (local_10 == '\x01') {
    *(short *)(param_1 + 0x115cb0) = *(short *)(param_1 + 0x115cb0) + 1;
    if (3 < *(short *)(param_1 + 0x115cb0)) {
      *(undefined2 *)(param_1 + 0x115cb0) = 0;
      *(short *)(param_1 + 0x115cae) = *(short *)(param_1 + 0x115cae) + 1;
      *(short *)(param_1 + 0x115cae) = *(short *)(param_1 + 0x115cae) % 0x168;
    }
  }
  else if (local_10 == '\x02') {
    local_8 = param_1;
    iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAppear.cpp",
                                DAT_00618ee0 + 0x1c,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  else {
    *(short *)(param_1 + 0x115cae) = *(short *)(param_1 + 0x115cae) + 2;
    *(short *)(param_1 + 0x115cae) = *(short *)(param_1 + 0x115cae) % 0x168;
    *(short *)(param_1 + 0x115cb0) = *(short *)(param_1 + 0x115cb0) + *(short *)(param_1 + 0x115cb2)
    ;
    if (0x2c < *(short *)(param_1 + 0x115cb0)) {
      *(short *)(param_1 + 0x115cb2) = -*(short *)(param_1 + 0x115cb2);
      *(undefined2 *)(param_1 + 0x115cb0) = 0x2d;
    }
    if (*(short *)(param_1 + 0x115cb0) < 0) {
      *(short *)(param_1 + 0x115cb2) = -*(short *)(param_1 + 0x115cb2);
      *(undefined2 *)(param_1 + 0x115cb0) = 0;
    }
  }
  local_8 = 0x482143;
  FUN__text__0056ce80();
  return;
}

