
/* WARNING: Removing unreachable block (ram,0x0045a705) */

void FUN__text__0045a5e0(void)

{
  code *pcVar1;
  undefined4 uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 uVar5;
  undefined4 uVar6;
  undefined4 uVar7;
  undefined4 uVar8;
  undefined4 local_dc [16];
  int local_9c;
  int local_98;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB__text__0058f96c;
  local_10 = ExceptionList;
  puVar4 = local_dc;
  for (iVar3 = 0x33; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  ExceptionList = &local_10;
  FUN__text__004075e0();
  local_8 = 0;
  FUN__text__0045a740();
  FUN__text__004077c0(DAT_007a49fc);
  local_98 = FUN__text__0042ae20("data\\test\\011101map3_00-00.dxp");
  if ((local_98 == 0) &&
     (iVar3 = FUN__text__00424f80("addr!=0","E:\\CrossHermit\\GAME\\src\\yoshida\\TestTask.cpp",
                                  DAT_0060ce8c + 0x1a,0), iVar3 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  uVar8 = 1;
  uVar7 = 1;
  uVar6 = 1;
  uVar5 = 0;
  iVar3 = local_98;
  uVar2 = FUN__text__004142b0(0,local_98,1,1,1);
  FUN__text__00404fb0(uVar2,uVar5,iVar3,uVar6,uVar7,uVar8);
  do {
    for (local_9c = 0; local_9c != 100; local_9c = local_9c + 1) {
      FUN__text__004079c0(local_9c * 2 + 100,local_9c * 2 + 100);
    }
    FUN__text__00422360(0);
  } while( true );
}

