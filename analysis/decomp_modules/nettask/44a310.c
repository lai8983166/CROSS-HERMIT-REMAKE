
void __fastcall FUN__text__0044a310(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [16];
  undefined2 local_10;
  undefined2 local_c;
  int local_8;
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = param_1;
  if ((*(char *)(param_1 + 0x1a8a) < '\0') || ('\x04' < *(char *)(param_1 + 0x1a8a))) {
    iVar2 = FUN__text__00424f80("(0<=NetData.Sce.ExtTabNo) && (NetData.Sce.ExtTabNo<=4)",
                                "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetTask.cpp",DAT_0060675c + 10
                                ,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_c = *(undefined2 *)(&DAT_00605e98 + *(char *)(local_8 + 0x1a8a) * 8);
  local_10 = *(undefined2 *)(&PTR_DAT_00605e9a + *(char *)(local_8 + 0x1a8a) * 2);
  FUN__text__0044cb40(local_8 + 0x38,CONCAT22(*(char *)(local_8 + 0x1a8a) >> 7,local_c),local_10,
                      0x56,5,&DAT_00605ef8 + *(char *)(local_8 + 0x1a8a) * 8);
  local_8 = 0x44a3d6;
  FUN__text__0056ce80();
  return;
}

