
void FUN__text__004dfb20(undefined4 param_1,int param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_48 [16];
  uint local_8;
  
  puVar3 = local_48;
  for (iVar2 = 0x11; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = (uint)(byte)(&DAT_006f4096)[param_2 * 0x10];
  if ((0x10 < local_8) &&
     (iVar2 = FUN__text__00424f80("(0<=off)&&(off<=16)",
                                  "E:\\CrossHermit\\GAME\\SRC\\Common\\ComYken.cpp",DAT_00738ca8 + 4
                                  ,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  local_8 = 0x4dfb9a;
  FUN__text__0056ce80();
  return;
}

