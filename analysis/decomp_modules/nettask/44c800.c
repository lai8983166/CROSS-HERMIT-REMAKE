
void FUN__text__0044c800(char param_1)

{
  code *pcVar1;
  char cVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_4c [16];
  int local_c;
  undefined4 local_8;
  
  puVar4 = local_4c;
  for (iVar3 = 0x12; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  if (((param_1 < '\0') || ('\x03' < param_1)) &&
     (iVar3 = FUN__text__00424f80("(0<=player_no) && (player_no<4)",
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetTask.cpp",
                                  DAT_00606798 + 3,0), iVar3 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  cVar2 = FUN__text__0041ad60();
  local_c = (int)cVar2;
  local_8 = 0x44c89f;
  FUN__text__0056ce80();
  return;
}

