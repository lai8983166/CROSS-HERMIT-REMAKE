
void __thiscall FUN__text__004277a0(int *param_1,int param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_48 [16];
  int *local_8;
  
  puVar3 = local_48;
  for (iVar2 = 0x11; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = param_1;
  if ((param_1[1] == 0) &&
     (iVar2 = FUN__text__00424f80("ListWork!=0",
                                  "e:\\crosshermit\\game\\src\\system\\syslinklist.cpp",
                                  DAT_005ff6a8 + 1,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  if ((*local_8 == 0) &&
     (iVar2 = FUN__text__00424f80("ListCnt!=0","e:\\crosshermit\\game\\src\\system\\syslinklist.cpp"
                                  ,DAT_005ff6a8 + 2,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  if ((*local_8 <= param_2) &&
     (iVar2 = FUN__text__00424f80("off<ListCnt",
                                  "e:\\crosshermit\\game\\src\\system\\syslinklist.cpp",
                                  DAT_005ff6a8 + 3,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  local_8 = (int *)0x427886;
  FUN__text__0056ce80();
  return;
}

