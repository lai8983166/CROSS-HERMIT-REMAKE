
void FUN__text__0044c000(int param_1,undefined4 param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [16];
  uint local_10;
  undefined4 local_c;
  undefined4 local_8;
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if ((param_1 < 0) || (1 < param_1)) {
    iVar2 = FUN__text__00424f80("(0<=type) && (type<=1)",
                                "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetTask.cpp",DAT_00606778 + 4,
                                0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_c = FUN__text__0044bed0(param_1);
  local_10 = -(uint)(param_1 != 0) & 0x40;
  FUN__text__0044c0a0(local_c,param_2);
  local_8 = 0x44c08b;
  FUN__text__0056ce80();
  return;
}

