
/* WARNING: Removing unreachable block (ram,0x0045e188) */

void FUN__text__0045e090(void)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_5e0 [16];
  undefined1 local_5a0;
  int local_59c;
  undefined4 local_598;
  undefined1 local_514 [1284];
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB__text__0058fa75;
  local_10 = ExceptionList;
  puVar3 = local_5e0;
  for (iVar2 = 0x174; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  ExceptionList = &local_10;
  _eh_vector_constructor_iterator_(local_514,0x80,10,FUN__text__004075e0,FUN__text__00407710);
  local_8 = 0;
  FUN__text__004075e0();
  local_8 = CONCAT31(local_8._1_3_,1);
  local_598 = 0;
  local_5a0 = 0;
  FUN__text__004150a0(0);
  FUN__text__004143a0(0,0,0);
  local_59c = FUN__text__00409240("data\\TACTICS\\Test\\BGTEST11.bmp",1,1,0);
  if (local_59c == 0) {
    iVar2 = FUN__text__00424f80("ret!=0","E:\\CrossHermit\\GAME\\src\\yoshida\\TestTask.cpp",
                                DAT_0060ce9c + 0xb,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  do {
    FUN__text__00422360(0);
  } while( true );
}

