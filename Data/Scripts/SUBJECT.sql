USE [SchemaCheck]
GO

/****** Object:  Table [dbo].[SUBJECTS]    Script Date: 12-01-2024 18:04:44 ******/
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[SUBJECTS]') AND type in (N'U'))
DROP TABLE [dbo].[SUBJECTS]
GO

/****** Object:  Table [dbo].[SUBJECTS]    Script Date: 12-01-2024 18:04:44 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[SUBJECTS](
	[ID] [uniqueidentifier] NOT NULL,
	[SUBJECT] [varchar](50) NOT NULL,
	[TABLE_NAME] [varchar](50) NOT NULL
) ON [PRIMARY]
GO


